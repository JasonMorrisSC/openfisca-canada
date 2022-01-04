from openfisca_core.model_api import not_
from openfisca_core.periods import DAY, YEAR, MONTH
from openfisca_core.variables import Variable


from openfisca_canada.entities import Person

# Presumption
# 4.1 If the Minister intends to waive the requirement for an application in respect of a person under subsection 5(4)
# and the information available to the Minister under this Act with respect to that person includes the prescribed 
# information, the person is presumed, in the absence of evidence to the contrary, to have met the requirements of
# (a) subparagraph 3(1)(b)(iii) or (c)(iii) or paragraph 3(2)(b); or
# (b) paragraph 4(1)(a) or (b).

# Semantically, it is difficult to parse what the "or" means between paragraph (a) and (b), here.
# Section 3 refers to the residence requirements for full and partial pension recipients.
# Section 4 creates an additional requirement that the residence was legal, and how to determine that.
# It is useless to determine that a person qualifies under 3 but not 4, or 4 but not 3.
# There is nothing about concluding that 3 is satisfied that requires you to preclude 4, or vice
# versa. As such, the "or" at the end of paragraph 4.1(a) is interpreted as conjunctive.
#
# The "or" inside paragraph (b), for example, is also strange. The person is deemed to have met
# the requirements of 4(1)(a) or (b), can mean, one, but not the other, or as many as are required.
# 4(1)(a) and (b) can both be true at the same time, and are disjunctive also.  That suggests that
# the use of "or" inside paragraph (b) is actually the typical logical use of disjunction, which
# implies that either both are true, or at least one is true, but in either case the requirement
# of 4(1) is satisfied.
#
# Similarly, 3(1)(b)(iii) and 3(1)(c)(iii) are mutually exclusive due to their context. The "or"
# in paragraph (a) is not exclusive, at least.
#
# So the meaning that is going to be encoded here is that if the conditions are satisfied,
# all five of those requirements can be "deemed" met.
#
# This unfortunately is another exception, which is going to require us to reformulate our
# encoding of those five sections to include the additional way of reaching the same conclusion.
#
# TODO: Update five sections above with new method of satisfying them.

class oas_s4_dot_1_satisfied(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "The Person is presumed to satisfy residence requirements under section 4.1 of the Old Age Security Act."

    def formula(person, period, parameters):
        minister_intends = person("oas_s4_dot_1_minister_intends_to_waive_requirement_for_application_under_oas_5_4", period)
        information_available = person("oas_s4_dot_1_prescribed_information_available_to_minister", period)
        absence_of_evidence_to_contrary = person("oas_s4_dot_1_absence_of_evidence_to_contrary", period)
        return minister_intends * information_available * absence_of_evidence_to_contrary

class oas_s4_dot_1_satisfied_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether we know if the Person is presumed to satisfy residence requirements under section 4.1 of the Old Age Security Act."

    def formula(person, period, parameters):
        minister_intends = person("oas_s4_dot_1_minister_intends_to_waive_requirement_for_application_under_oas_5_4", period)
        minister_intends_known = person("oas_s4_dot_1_minister_intends_to_waive_requirement_for_application_under_oas_5_4_known", period)
        information_available = person("oas_s4_dot_1_prescribed_information_available_to_minister", period)
        information_available_known = person("oas_s4_dot_1_prescribed_information_available_to_minister_known", period)
        absence_of_evidence_to_contrary = person("oas_s4_dot_1_absence_of_evidence_to_contrary", period)
        absence_of_evidence_to_contrary_known = person("oas_s4_dot_1_absence_of_evidence_to_contrary_known", period)
        # A conjunction is known if any of its elements is known false or all elements are known.
        all_known = minister_intends_known * information_available_known * absence_of_evidence_to_contrary_known
        any_false = (not_(minister_intends) * minister_intends_known) + \
                    (not_(information_available) * information_available_known) + \
                    (not_(absence_of_evidence_to_contrary) * absence_of_evidence_to_contrary_known)
        return all_known + any_false

# The remainder of the variables in this section will be treated as inputs.
# It is possible that there is a policy setting out when the Minister will waive
# the requirement of an application, and this section might end up reformulated
# if we attempted to encode those policies.
#
# The presribed information is something set out in the regulations, and it would
# be possible to encode more deeply, also, if we needed it.
#
# The existence of evidence to the contrary is something that is unlikely to be
# honestly reported by a user motivated to qualify, and is useful only for
# people capable of exercising discretion over whether that evidence exists.
# Specific examples could be encoded, but the list would not be exhaustive, and
# so we would need to leave it as an input variable regardless. I'm also not
# aware of any specific examples in statute anywhere, so we would be encoding
# something other than rules, at that point.

class oas_s4_dot_1_minister_intends_to_waive_requirement_for_application_under_oas_5_4(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the Minister intends to waive the requirement for an application with regard to the person under oas 5(4)."

class oas_s4_dot_1_minister_intends_to_waive_requirement_for_application_under_oas_5_4_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether it is known if the Minister intends to waive the requirement for an application with regard to the person under oas 5(4)."

class oas_s4_dot_1_prescribed_information_available_to_minister(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the the prescribed information is available to the minister under section 4.1 of the OAS."

class oas_s4_dot_1_prescribed_information_available_to_minister_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether it is known if the the prescribed information is available to the minister under section 4.1 of the OAS."

class oas_s4_dot_1_absence_of_evidence_to_contrary(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether there is an absence of evidence that the person's residence is not valid."

class oas_s4_dot_1_absence_of_evidence_to_contrary_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether it is known if there is an absence of evidence that the person's residence is not valid."

