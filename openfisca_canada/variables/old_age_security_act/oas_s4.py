from openfisca_core.model_api import not_
from openfisca_core.periods import DAY, YEAR, MONTH
from openfisca_core.variables import Variable
from openfisca_core.indexed_enums import Enum
from datetime import date, datetime
from numpy import bool, float, int, str, where, isin, floor

from openfisca_canada.entities import Person

# Residence in Canada must be or have been legal
# 4 (1) A person who was not a pensioner on July 1, 1977 is eligible for a pension 
# under this Part only if
# (a) on the day preceding the day on which that person’s application is approved 
# that person is a Canadian citizen or, if not, is legally resident in Canada; or
# (b) on the day preceding the day that person ceased to reside in Canada that person 
# was a Canadian citizen or, if not, was legally resident in Canada.

# Because this is an overriding provision, that can interfere with any other provision that would deem the person
# eligible for a pension under this part, this code now needs to be used in the formula for any other variable
# that sets out eligibility explicitly. It's not clear yet which provisions those are.

# TODO: Make sure section 4 is considered in all Part II eligibility statements.

class oas_s4_1_satisfied(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "In accordance with section 4(1) the person is eligible to receive a pension under Part I of the Old Age Security Act."

    def formula(person, period, parameters):
        not_pensioner = not_(person('oas_s2_pensioner',1977_07_01))
        suba = person('oas_s4_1_a_satisfied', period)
        subb = person('oas_s4_1_b_satisfied', period)
        return not_pensioner * (suba + subb)

class oas_s4_1_satisfied_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether we know if accordance with section 4(1) the person is eligible to receive a pension under Part I of the Old Age Security Act."

    def formula(person, period, parameters):
        not_pensioner_reversed = person('oas_s2_pensioner',1977_07_01)
        not_pensioner_known = person('oas_s2_pensioner_known',1977_07_01)
        suba = person('oas_s4_1_a_satisfied', period)
        suba_known = person('oas_s4_1_a_satisfied_known', period)
        subb = person('oas_s4_1_b_satisfied', period)
        subb_known = person('oas_s4_1_b_satisfied_known', period)
        # The disjunction is known if either is known true or both are known
        sub_any_false = (suba * suba_known) + (subb * subb_known)
        sub_all_known = suba_known * subb_known
        sub_known = sub_any_false + sub_all_known
        # The conjunction is known if either is known false or both are known
        any_false = (not_pensioner_reversed * not_pensioner_known) + (not_(suba + subb) * sub_known)
        all_known = not_pensioner_known * sub_known
        return any_false + all_known

# (a) on the day preceding the day on which that person’s application is approved 
# that person is a Canadian citizen or, if not, is legally resident in Canada; or

class oas_s4_1_a_satisfied(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether section 4(1)(a) is satisfied, and the person was citizen or legally resident the day before approval."

    def formula(person, period, parameters):
        approval = person("oas_s3_approval_date",period) # I am re-using the s3 definition, but perhaps this should be elevated if it will be re-used a lot
        citizen = person("legal_status", approval.previous_day) == "CANADIAN_CITIZEN"
        legally_resident = person("oas_s4_legally_resident_in_canada", approval.previous_day)
        return citizen + legally_resident

class oas_s4_1_a_satisfied_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether it is known if section 4(1)(a) is satisfied, and the person was citizen or legally resident the day before approval."

    def formula(person, period, parameters):
        # A disjunction is known if either element is known true, or both are known. Approval also needs to be known.
        approval_known = person("oas_s3_approval_date_known", period)
        approval = person("oas_s3_approval_date",period)
        either_true = ((person("legal_status", approval.previous_day) == "CANADIAN_CITIZEN") * person("legal_status_known", approval.previous_day)) + \
                        (person("oas_s4_legally_resident_in_canada", approval.previous_day) * person("oas_s4_legally_resident_in_canada_known", approval.previous_day))
        both_known = person("legal_status_known", approval.previous_day) * person("oas_s4_legally_resident_in_canada_known", approval.previous_day)
        return approval_known * ( either_true + both_known )

# (b) on the day preceding the day that person ceased to reside in Canada that person 
# was a Canadian citizen or, if not, was legally resident in Canada.

class oas_s4_1_b_satisfied(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether section 4(1)(b) is satisfied, and the person was citizen or legally resident the day before ceasing to reside in Canada."

    def formula(person, period, parameters):
        date_ceasing_to_reside = person("ceasing_to_reside_in_canada_date", period)
        citizen = person("legal_status", date_ceasing_to_reside.previous_day) == "CANADIAN_CITIZEN"
        legally_resident = person("oas_s4_legally_resident_in_canada", date_ceasing_to_reside.previous_day)
        return citizen + legally_resident

class oas_s4_1_b_satisfied_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether it is known if section 4(1)(b) is satisfied, and the person was citizen or legally resident the day before ceasing to reside in Canada."

    def formula(person, period, parameters):
        # A disjunction is known if either element is known true, or both are known. Approval also needs to be known.
        date_ceasing_to_reside = person("ceasing_to_reside_in_canada_date", period)
        date_ceasing_to_reside_known = person("ceasing_to_reside_in_canada_date_known", period)
        either_true = ((person("legal_status", date_ceasing_to_reside.previous_day) == "CANADIAN_CITIZEN") * person("legal_status_known", date_ceasing_to_reside.previous_day)) + \
                        (person("oas_s4_legally_resident_in_canada", date_ceasing_to_reside.previous_day) * person("oas_s4_legally_resident_in_canada_known", date_ceasing_to_reside.previous_day))
        both_known = person("legal_status_known", date_ceasing_to_reside.previous_day) * person("oas_s4_legally_resident_in_canada_known", date_ceasing_to_reside.previous_day)
        return date_ceasing_to_reside_known * ( either_true + both_known )

# Regulations respecting legal residence
# (2) The Governor in Council may make regulations respecting the meaning of legal 
# residence for the purposes of subsection (1).

# This is problematic in a number of ways. First, we probably don't need to actually test 
# for whether or not the GiC acted within its jurisdiction,
# so the substantive meaning of this section, which is an enabling provision, doesn't need
# to be encoded for our purposes. If it did, we would need a higher-level set of concepts
# in order to model permissions to enact rules, and then we would need to represent the rules
# in a reified way so that we could associate them with the people who enacted them, and check
# to see if they had capacity at the time. Even if you could get that far, you are still left
# with the problem that the boundaries on the authority are purposive, and it is virtually
# impossible to detect the purpose of an encoding from its semantic representation.

# That said, this section practically means that the definition of "legally resident" used in s4(1)(a) and (b)
# is defined by whether or not the definition set out in the regulations is satisfied.
# We encode that idea as follows.

class oas_s4_legally_resident_in_canada(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether for the purposes of section 4, the person was legally resident in Canada."

    def formula(person, period, parameters):
        return person("oas_s4_2_legal_residence_according_to_regulations_satisfied", period)

class oas_s4_legally_resident_in_canada_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether we know if for the purposes of section 4, the person was legally resident in Canada."

    def formula(person, period, parameters):
        return person("oas_s4_2_legal_residence_according_to_regulations_satisfied_known", period)

class oas_s4_2_legal_residence_according_to_regulations_satisfied(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether under the regulations enacted under s4(2) of the OAS, the person was legally resident in Canada."

class oas_s4_2_legal_residence_according_to_regulations_satisfied_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether under the regulations enacted under s4(2) of the OAS, the person was legally resident in Canada."

# The problem with this approach is that now if a regulation is added to the regime, it will need to be reflected here, in
# the code that refers to the regulation. It may not be possible to override. Because this version is an input variable
# you could conceivably override the class definition once with a function definition, and have that work, but the
# code for the regulation would need to refer to oas_s4_2..., and it wouldn't work twice. So for consistency, any
# time the cross referenced legislation changes, you will need to check and see if this code needs to change, too.

# As it happens, it seems that the relevant section of code is section 22 of the Old Age Security Regulations.
# A stub file has been created for those rules.