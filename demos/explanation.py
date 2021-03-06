import requests
import json
from pprint import pprint
import networkx as nx
from networkx import descendants, all_simple_paths
from numpy import unique

# From inside the root of this repository, run `pip install .` followed by
# `openfisca serve` to run the WebAPI locally.
# You will also need to `pip install networkx`.

# The trace endpoint is used to get access to information about dependencies
# between variables. If you do not need explanations, the /calculate
# endpoint will provide the same answers, and potentially faster.

target = "http://localhost:5000/trace"

# Create a dictionary representing the facts that will be sent
# to the API. Here, we describe a situation with one person,
# who is of age 40. Note that whenever you specify a variable,
# you must also explicitly tell OpenFisca that you are doing so.
# Without that information it cannot determine whether or not
# to be confident in the answers it generates.
#
# You pose a query by including variables with a null value in
# the JSON, which is accomplished by making them None in the dictionary.
# Here, we are asking for two outputs:
# oas_eligible - tells us whether or not the person is eligible for OAS
# oas_eligible_known - tells us whether OpenFisca is certain of the result

facts = {
    "persons": {
        "person1": {
            "age": {
                "2021-12-01": 65
            },
            "age_known": {
                "2021-12-01": True
            },
            "oas_eligible": {
                "2021-12-01": None
            },
            "oas_eligible_known": {
                "2021-12-01": None
            }
        },
        "person2": {
            "age": {
                "2021-12-01": 65
            },
            "age_known": {
                "2021-12-01": True
            },
            "income": {
                "2021": 10000
            },
            "income_known": {
                "2021": True
            },
            "place_of_residence": {
                "2021-12-01": "GR"
            },
            "place_of_residence_known": {
                "2021-12-01": True
            },
            "years_in_canada_since_18": {
                "2021-12-01": 20
            },
            "years_in_canada_since_18_known": {
                "2021-12-01": True
            },
            "legal_status": {
                "2021-12-01": "CANADIAN_CITIZEN"
            },
            "legal_status_known": {
                "2021-12-01": True
            },
            "oas_eligible": {
                "2021-12-01": None
            },
            "oas_eligible_known": {
                "2021-12-01": None
            }
        }
    }
}


payload = json.dumps(facts)

headers = {}
headers["Accept"] = "application/json"
headers["Content-Type"] = "application/json"

r = requests.post(target,data=payload,headers=headers)

response = json.loads(r.text)
# pprint(response)

# The JSON package returned from /trace has the following parts:
# entitiesDescription is a dictionary of entity types, each of which
# is a list of entities of that type included in the data.
# For example: {'persons': ['person1']}
# 
# requestedCalculations is a list of the variables OpenFisca attempted
# to calculate.
# For example: ['oas_eligible<2021-12-01>','oas_eligible_known<2021-12-01>']
#
# trace is a dictionary of variables that were used in the calculation.
# each variable is a dictionary that includes the following relevant parts:
# * dependencies
# * parameters
# * value
#
# Within "trace", dependencies is a list of  variables that were used in calculating the parent,
# in the variable_name<period> format.
#
# Parameters is a dictionary of parameters that were used in the calculation.
# This is difficult to process, because there is no guarantee about the data type
# returned by the parameter. It may be scalar, or a list, or something else.
# For our purposes we will not try to use parameters in explanations.
#
# The value is the list of values that was calculated for the variable by OpenFisca.
# Remember that OpenFisca is expecting to get a list of entities to do calculations
# for, and returns the values for each variable as a list of the value calculated
# for each entity, respectively.
#
# In order to generate an explanation from this data, we create a graph. Each
# trace element becomes a node in the graph. Each dependency becomes a vector.
# Each node is given its value, and its corresponding known value.

dependency_graph = nx.DiGraph()
for (K,V) in response['trace'].items():
    if "_known<" not in K: # Exlclude _known variables, as they will be used to annotate
        dependency_graph.add_node(K, value=V['value'])
        for target in V['dependencies']:
            dependency_graph.add_edge(K,target)
for (K,V) in response['trace'].items():
    if "_known<" in K:
        related_node = K.replace("_known<","<")
        dependency_graph.nodes[related_node]['known'] = V['value']

from pprint import pprint


# The above creates a network of nodes, each of which has a 'value' and a 'known' attribute,
# and edges from each variable to the variables on which it depended.

# Now we can go through all the nodes in the graph and add a third value called 'display'
# that will include the value if it is known, and the string "unknown" otherwise.

# Note that there is something about the above algorithm that generates
# duplicate nodes with no attributes, so we use the incorrect_nodes list
# below to remove them, which seems to solve the problem.

incorrect_nodes = []
for N in dependency_graph:
    # Not sure why this test is necessary, but duplicate nodes
    # with no value show up for root elements in the graph
    if 'value' in dependency_graph.nodes[N]:
      values = dependency_graph.nodes[N]['value']
      if 'known' in dependency_graph.nodes[N]:
        knowns = dependency_graph.nodes[N]['known']
      else: # Some output variables do not have associated "known" variables.
        knowns = [True] * len(values)
        dependency_graph.nodes[N]['known'] = knowns
      display = []
      for (value, known) in zip(values,knowns):
          display.append(value if known else "unknown, potentially " + str(value))
      dependency_graph.nodes[N]['display'] = display
    else:
      incorrect_nodes.append(N)

for i in incorrect_nodes:
  dependency_graph.remove_node(i)

## Now we can use the graph to do complicated things. First, we use it to generate a
# natural langauge explanation for how each conclusion requested was reached.

# We start by defining a recursive algorithm that generates the text of the explanation
# from the graph given a starting node, and the index of the entity that the explanation
# is for. Remember that all "values" in the data are actually a list of values, one
# for each entity included.


def generate_explanation(goal,entity,index=0):
    indent = ' ' * index
    because = ', because' if len(dependency_graph.adj[goal]) else ', and'
    output = ""
    output += indent + goal.replace("<", " as of ").replace(">", "") + " is " + str(dependency_graph.nodes[goal]['display'][entity]) + because + '\n'
    index += 2
    for neighbour in dependency_graph.adj[goal]:
        output += generate_explanation(neighbour,entity,index)
    return output


#pprint(adjacency_data(dependency_graph))

# Now we find the name of the variables we were actually looking for,
# eliminate the "known" variables, and process the results for each


from networkx import all_simple_paths

for goal in unique(response['requestedCalculations']):
    if "_known<" not in goal:
        print("--------------------------------------")
        i = 0
        while i < len(dependency_graph.nodes[goal]['value']):
            print("For Entity #" + str(i+1) + ":")
            
            # We can use the graph to determine what input variables remain relevant.
            # An input variable is a variable with no descendents in the dependency graph.
            # It is relevant if it is not descendent of a "known" variable.

            relevant = []

            for node in descendants(dependency_graph,goal):
                if not descendants(dependency_graph,node): # Only leaf nodes
                    if not dependency_graph.nodes[node]['known'][i]:
                      known_parent = False
                      for path in all_simple_paths(dependency_graph,goal,node):
                        for parent in path:
                            if dependency_graph.nodes[parent]['known'][i] == True:
                                known_parent = True
                                break
                        if not known_parent:
                            relevant.append(node)

            # If we know which input variables will not be collected by the interface, and the
            # list of relevant variables is exclusively from that list, we can infer that the
            # conclusion is contingent on things we won't collect, and advise the user
            # accordingly. Note that you will need to generate the list
            # with the same period used in the inputs.
            
            unaskable = ['eligible_under_social_agreement<2021-12-01>']
            conditional = False
            relevant_and_askable = False
            if relevant:
              for q in relevant:
                if q not in unaskable:
                    relevant_and_askable = True
              if not relevant_and_askable and dependency_graph.nodes[goal]['known'][i] == False:
                conditional = True
                dependency_graph.nodes[goal]['display'][i] = "conditionally known, potentially " + str(dependency_graph.nodes[goal]['value'][i])

            # Now we can generate an explanation with the changes above,
            # and display it to the user along with the other useful information.
                
            explanation = generate_explanation(goal,i)[:-6] # The slice removes the trailing ", and\n"
            
            print(explanation)
            if conditional:
              print("The conclusion is conditionally known, because all remaining relevant inputs are not askable.")
            print("The remaining relevant inputs are " + str(unique(relevant)))
            
            
            i += 1