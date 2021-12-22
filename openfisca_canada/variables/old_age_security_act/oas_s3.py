from openfisca_core.model_api import not_
from openfisca_core.periods import DAY, YEAR, MONTH
from openfisca_core.variables import Variable
from openfisca_core.indexed_enums import Enum
from datetime import date, datetime
from numpy import bool, float, int, str, where, isin, floor

from openfisca_canada.entities import Person

## Section 3(1)

# 3 (1) Subject to this Act and the regulations, a full monthly pension may be paid to
# (a) every person who was a pensioner on July 1, 1977;
# (b) every person who
# (i) on July 1, 1977 was not a pensioner but had attained twenty-five years of age and resided in Canada or, if that person did not reside in Canada, had resided in Canada for any period after attaining eighteen years of age or possessed a valid immigration visa,
# (ii) has attained sixty-five years of age, and
# (iii) has resided in Canada for the ten years immediately preceding the day on which that person’s application is approved or, if that person has not so resided, has, after attaining eighteen years of age, been present in Canada prior to those ten years for an aggregate period at least equal to three times the aggregate periods of absence from Canada during those ten years, and has resided in Canada for at least one year immediately preceding the day on which that person’s application is approved; and
# (c) every person who
# (i) was not a pensioner on July 1, 1977,
# (ii) has attained sixty-five years of age, and
# (iii) has resided in Canada after attaining eighteen years of age and prior to the day on which that person’s application is approved for an aggregate period of at least forty years.


# > 3 (1) Subject to this Act and the regulations, a full monthly pension may be paid to
# OpenFisca does not provide a mechanism for encoding defeasibility, so the "subject to" line is
# not encoded. All relevant sections of the act and regulations would need to be combined into the
# variable definitions.
#
# section 3(1) sets out that a full monthly pension may be paid to a person if 3(1)(a-c) apply.

class oas_s3_1_satisfied(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "In accordance with section 3(1) of the Old Age Security Act, the person may be paid a full monthly pension."

    def formula(person, period, parameters):
        """Whether the person may, under section 3(1) of the Old Age Security Act, be paid a full monthly pension."""
        # Qualify under 3(1)(a),
        suba = person("oas_s3_1_a_satisfied", period)
        # QUalify under 3(1)(b), or
        subb = person("oas_s3_1_b_satisfied", period)
        # Qualify under 3(1)(c)
        subc = person("oas_s3_1_c_satisfied", period)
        return  suba + subb + subc

class oas_s3_1_satisfied_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether it is known if, in accordance with section 3(1) of the Old Age Security Act, the person may be paid a full monthly pension."

    def formula(person, period, parameters):
        """Whether it is known if the person may, under section 3(1) of the Old Age Security Act, be paid a full monthly pension."""
        # Qualify under 3(1)(a),
        suba = person("oas_s3_1_a_satisfied", period)
        suba_known = person("oas_s3_1_a_satisfied_known", period)
        # QUalify under 3(1)(b), or
        subb = person("oas_s3_1_b_satisfied", period)
        subb_known = person("oas_s3_1_b_satisfied_known", period)
        # Qualify under 3(1)(c)
        subc = person("oas_s3_1_c_satisfied", period)
        subc_known = person("oas_s3_1_c_satisfied_known", period)
        # A disjunciton is known if any of the elements are known true, or
        # all the elements are known.
        any_true = (suba * suba_known) + (subb * subb_known) + (subc * subc_known)
        all_known = suba_known * subb_known * subc_known
        return  any_true + all_known


# (a) every person who was a pensioner on July 1, 1977;
# Straightforward reference to the definition of "pensioner" in section 2 as of a specific date.

class oas_s3_1_a_satisfied(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "The person satisfies section 3(1)(a) of the Old Age Security Act, as they were a pensioner on July 1, 1977."

    def formula(person, period, parameters):
        """Whether the person was, on July 1, 1977, a pensioner."""
        # every person who was a pensioner on July 1, 1977;
        return person("oas_s2_pensioner_satisfied", 1977_7_1) #Is this period syntax correct?

class oas_s3_1_a_satisfied_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether it is known if he person satisfies section 3(1)(a) of the Old Age Security Act, as they were a pensioner on July 1, 1977."

    def formula(person, period, parameters):
        """Whether it is known if the person was, on July 1, 1977, a pensioner."""
        # every person who was a pensioner on July 1, 1977;
        return person("oas_s2_pensioner_satisfied_known", 1977_7_1) #Is this period syntax correct?


# (b) every person who
# (i) on July 1, 1977 was not a pensioner but had attained twenty-five years of age and resided in Canada or, if that person did not reside in Canada, had resided in Canada for any period after attaining eighteen years of age or possessed a valid immigration visa,
# (ii) has attained sixty-five years of age, and
# (iii) has resided in Canada for the ten years immediately preceding the day on which that person’s application is approved or, if that person has not so resided, has, after attaining eighteen years of age, been present in Canada prior to those ten years for an aggregate period at least equal to three times the aggregate periods of absence from Canada during those ten years, and has resided in Canada for at least one year immediately preceding the day on which that person’s application is approved; and

class oas_s3_1_b_satisfied(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "The person meeds the definition of section 3(1)(b) of the Old Age Security Act."

    def formula(person, period, parameters):
        """Whether the person is caught under section 3(1)(b) of the Old Age Security Act."""
        #Qualify under 3(1)(b)(i),
        subi = person("oas_s3_1_b_i_satisfied", period)
        #QUalify under 3(1)(b)(ii), and
        subii = person("oas_s3_1_b_ii_satisfied", period)
        #Qualify under 3(1)(b)(iii)
        subiii = person("oas_s3_1_b_iii_satisfied", period)
        return subi * subii * subiii


class oas_s3_1_b_satisfied_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether it is known if the person meeds the definition of section 3(1)(b) of the Old Age Security Act."

    def formula(person, period, parameters):
        """Whether it is known if the person is caught under section 3(1)(b) of the Old Age Security Act."""
        #Qualify under 3(1)(b)(i),
        subi = person("oas_s3_1_b_i_satisfied", period)
        subi_known = person("oas_s3_1_b_i_satisfied_known", period)
        #QUalify under 3(1)(b)(ii), and
        subii = person("oas_s3_1_b_ii_satisfied", period)
        subii_known = person("oas_s3_1_b_ii_satisfied_known", period)
        #Qualify under 3(1)(b)(iii)
        subiii = person("oas_s3_1_b_iii_satisfied", period)
        subiii_known = person("oas_s3_1_b_iii_satisfied_known", period)
        # A conjunction is known if any is known false, or all are known
        any_false = (not_(subi) * subi_known) + (not_(subii) * subii_known) + (not_(subiii) * subiii_known)
        all_known = subi_known * subii_known * subiii_known
        return any_false + all_known

# (i) on July 1, 1977 was not a pensioner but had attained twenty-five years of age
# and resided in Canada or, if that person did not reside in Canada, had resided in 
# Canada for any period after attaining eighteen years of age or possessed a valid 
# immigration visa,
#
# All of:
#  - Not a pensioner as of July 1, 1977
#  - All of:
#    - at least 25 years of age as of July 1, 1977
#    - One of:
#       - resided in canada as of July 1, 1977
#       - All of:
#         - did not reside in canada as of July 1, 1977
#         - One of:
#           - resided in canada for any period after 18 years of age as of July 1, 1977
#           - possessed a valid immigration visa as of July 1, 1977
#
# If we were to remove the "not pensioner" requirement, then a person might qualify under
# subparagraphs 3(1)(a) and 3(1)(b) at the same time, which is not what the law says.
# If we were to remove the redundant "did not reside in Canada", then a person might qualify
# under section 3(1)(b) both because they resided in Canada, and because they previously
# resided in Canada after the age of 18. Again, that is not what the law says. The law 
# as written allows
# only one of those conclusions to be reached at the same time.
#
# This is a particularly frustrating example, because in all likelihood the phrase "or if
# that person did not reside in Canada" is included so that the word "or" on its own would
# not be perceived as having the second half of the paragraph be alternative to the age
# requirement. Had the section been drafted in a more structured way, those extra words would
# be irrelevant, and there would be no need to encode it as an exclusive disjunction.
#
# So in the interests of fidelity to the text of the law, and providing explanations consistent
# with that text, we will encode the more complicated version.

class oas_s3_1_b_i_satisfied(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "The person meets the definition of section 3(1)(b)(i) of the Old Age Security Act."

    def formula(person, period, parameters):
        """Whether the person meets the definition of section 3(1)(b)(i) of the Old Age Security Act."""
        # All of:
        #  - Not a pensioner as of July 1, 1977
        #  - All of:
        #    - at least 25 years of age as of July 1, 1977
        #    - One of:
        #       - resided in canada as of July 1, 1977
        #       - All of:
        #         - did not reside in canada as of July 1, 1977
        #         - One of:
        #           - resided in canada for any period after 18 years of age as of July 1, 1977
        #           - possessed a valid immigration visa as of July 1, 1977
        not_pensioner_requirement = not_(person("oas_s2_pensioner_satisfied", 1977_07_01))
        age_and_residence_requirement = person("oas_s3_1_b_i_age_residence_satisfied", 1977_07_01)
        return not_pensioner_requirement * age_and_residence_requirement

class oas_s3_1_b_i_satisfied_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether we know if the person meets the definition of section 3(1)(b)(i) of the Old Age Security Act."

    def formula(person, period, parameters):
        """Whether we know if the person meets the definition of section 3(1)(b)(i) of the Old Age Security Act."""
        # All of:
        #  - Not a pensioner as of July 1, 1977
        #  - All of:
        #    - at least 25 years of age as of July 1, 1977
        #    - One of:
        #       - resided in canada as of July 1, 1977
        #       - All of:
        #         - did not reside in canada as of July 1, 1977
        #         - One of:
        #           - resided in canada for any period after 18 years of age as of July 1, 1977
        #           - possessed a valid immigration visa as of July 1, 1977
        not_pensioner_requirement_reversed = person("oas_s2_pensioner_satisfied", 1977_07_01)
        # I'm avoiding a double-negation here by testing for the original, and naming it reversed.
        # I'm not sure if that matters or not. In numpy, I doubt it would.
        not_pensioner_requirement_known = person("oas_s2_pensioner_satisfied_known", 1977_07_01)
        age_and_residence_requirement = person("oas_s3_1_b_i_age_residence_satisfied", 1977_07_01)
        age_and_residence_requirement_known = person("oas_s3_1_b_i_age_residence_satisfied_known", 1977_07_01)
        # A conjunction is known if any part is known false or all parts are known
        any_false = (not_pensioner_requirement_reversed * not_pensioner_requirement_known) + \
                    (not_(age_and_residence_requirement) * age_and_residence_requirement_known)
        all_known = not_pensioner_requirement_known * age_and_residence_requirement_known
        return  any_false + all_known

class oas_s3_1_b_i_age_residence_satisfied(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the person meets the age and residence requirement of section 3(1)(b)(i) of the Old Age Security Act."

    def formula(person, period, parameters):
        """Whether the person meets the age and residence requirement of section 3(1)(b)(i) of the Old Age Security Act."""
        #  - All of:
        #    - at least 25 years of age as of July 1, 1977
        #    - One of:
        #       - resided in canada as of July 1, 1977
        #       - All of:
        #         - did not reside in canada as of July 1, 1977
        #         - One of:
        #           - resided in canada for any period after 18 years of age as of July 1, 1977
        #           - possessed a valid immigration visa as of July 1, 1977
        attained_25_yoa = person("oas_s3_1_b_i_attained_25_years", 1977_07_01)
        residence_requirement = person("oas_s3_1_b_i_residence_requirement", 1977_07_01)
        return attained_25_yoa * residence_requirement

# Naming convention:
# Abbrevation for the act: oas
# Full section path with underscores: s3_1_b_i
# If it is not a sub-section of that path, the word "satisfied": satisfied
# If it is a sub-section of that path, a description for the sub-section: attained_25_years

class oas_s3_1_b_i_age_residence_satisfied_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether it is known if the person meets the age and residence requirement of section 3(1)(b)(i) of the Old Age Security Act."

    def formula(person, period, parameters):
        """Whether it is known if the person meets the age and residence requirement of section 3(1)(b)(i) of the Old Age Security Act."""
        #  - All of:
        #    - at least 25 years of age as of July 1, 1977
        #    - One of:
        #       - resided in canada as of July 1, 1977
        #       - All of:
        #         - did not reside in canada as of July 1, 1977
        #         - One of:
        #           - resided in canada for any period after 18 years of age as of July 1, 1977
        #           - possessed a valid immigration visa as of July 1, 1977
        attained_25_yoa = person("oas_s3_1_b_i_attained_25_years", 1977_07_01)
        attained_25_yoa_known = person("oas_s3_1_b_i_attained_25_years_known", 1977_07_01)
        residence_requirement = person("oas_s3_1_b_i_residence_requirement", 1977_07_01)
        residence_requirement_known = person("oas_s3_1_b_i_residence_requirement_known", 1977_07_01)
        # A conjunction is known if either part is known false or all are known
        any_false = (not_(attained_25_yoa) * attained_25_yoa_known) + \
                    (not_(residence_requirement) * residence_requirement_known)
        all_known = attained_25_yoa_known * residence_requirement_known
        return any_false + all_known

# Why model "attaining 25 years" as a variable, instead of including it as a
# test of person("age",date) >= 25?
# If we include it as a variable, then in the explanation, the user will see
# a variable named "attained 25 years", and a value of true or false, and reasons.
# If we do not, the user will see a variable named "met age and residence requirements"
# and will see a true or false, and an age, but will have no context with which to
# understand why age 25 was insufficient. OpenFisca provides no way to expose the fact
# that the test applied inside the formula was "greater than or equal to". Creating
# another variable makes that fact apparent in the explanations generated in the /trace
# API end-point.
#
# This need to create variables every time something happens inside the reasoning, be
# it a conjunction, disjunction, or comparison, in order to expose that knowledge to the
# user, is a major downside of using OpenFisca for explainable encodings.

class oas_s3_1_b_i_attained_25_years(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the person had attained the age of 25 as required by section 3(1)(b)(i) of the Old Age Security Act."

    def formula(person, period, parameters):
        """Whether the person had attained the age of 25 as required by section 3(1)(b)(i) of the Old Age Security Act."""
        return person("age",1977_07_01) >= 25

class oas_s3_1_b_i_attained_25_years_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether it is known if the person had attained the age of 25 as required by section 3(1)(b)(i) of the Old Age Security Act."

    def formula(person, period, parameters):
        """Whether it is known if the person had attained the age of 25 as required by section 3(1)(b)(i) of the Old Age Security Act."""
        return person("age_known",1977_07_01)

class oas_s3_1_b_i_residence_requirement(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the person satisfies the residence requirements of section 3(1)(b)(i) of the Old Age Security Act."

    def formula(person, period, parameters):
        """Whether the person satisfies the residence requirements of section 3(1)(b)(i) of the Old Age Security Act."""
        #    - One of:
        #       - resided in canada as of July 1, 1977
        #       - All of:
        #         - did not reside in canada as of July 1, 1977
        #         - One of:
        #           - resided in canada for any period after 18 years of age as of July 1, 1977
        #           - possessed a valid immigration visa as of July 1, 1977
        resided = person("oas_s3_1_b_i_resided_in_canada", 1977_07_01)
        alternative = person("oas_s3_1_b_i_non_resident_qualification", 1977_07_01)
        return resided + alternative

class oas_s3_1_b_i_residence_requirement_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the person satisfies the residence requirements of section 3(1)(b)(i) of the Old Age Security Act."

    def formula(person, period, parameters):
        """Whether the person satisfies the residence requirements of section 3(1)(b)(i) of the Old Age Security Act."""
        #    - One of:
        #       - resided in canada as of July 1, 1977
        #       - All of:
        #         - did not reside in canada as of July 1, 1977
        #         - One of:
        #           - resided in canada for any period after 18 years of age as of July 1, 1977
        #           - possessed a valid immigration visa as of July 1, 1977
        resided = person("oas_s3_1_b_i_resided_in_canada", 1977_07_01)
        resided_known = person("oas_s3_1_b_i_resided_in_canada_known", 1977_07_01)
        alternative = person("oas_s3_1_b_i_non_resident_qualification", 1977_07_01)
        alternative_known = person("oas_s3_1_b_i_non_resident_qualification_known", 1977_07_01)
        # A disjunction is known if any element is known true or if all elements are known.
        any_true = (resided * resided_known) + (alternative * alternative_known)
        all_known = resided_known * alternative_known
        return any_true + all_known

class oas_s3_1_b_i_resided_in_canada(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the person resided in Canada on July 1, 1977 as required by section 3(1)(b)(i) of the Old Age Security Act."

    def formula(person, period, parameters):
        """Whether the person resided in Canada on July 1, 1977 as required by section 3(1)(b)(i) of the Old Age Security Act."""
        return person("place_of_residence",1977_07_01) == "CA"


class oas_s3_1_b_i_resided_in_canada_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether it is known if the person resided in Canada on July 1, 1977 as required by section 3(1)(b)(i) of the Old Age Security Act."

    def formula(person, period, parameters):
        """Whether it is known if the person resided in Canada on July 1, 1977 as required by section 3(1)(b)(i) of the Old Age Security Act."""
        return person("place_of_residence_known",1977_07_01)

class oas_s3_1_b_i_non_resident_qualification(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the person met the alternative residence requirements on July 1, 1977 as required by section 3(1)(b)(i) of the Old Age Security Act."

    def formula(person, period, parameters):
        """Whether the person met the alternative residence requirements on July 1, 1977 as required by section 3(1)(b)(i) of the Old Age Security Act."""
        #       - All of:
        #         - did not reside in canada as of July 1, 1977
        #         - One of:
        #           - resided in canada for any period after 18 years of age as of July 1, 1977
        #           - possessed a valid immigration visa as of July 1, 1977
        not_resident = not_(person("oas_s3_1_b_i_resided_in_canada", 1977_07_01))
        resided_after_18_or_visa = person("oas_s3_1_b_i_resided_in_canada_after_18_or_had_visa", 1977_07_01)
        return not_resident * resided_after_18_or_visa

class oas_s3_1_b_i_non_resident_qualification_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether it is known if the person met the alternative residence requirements on July 1, 1977 as required by section 3(1)(b)(i) of the Old Age Security Act."

    def formula(person, period, parameters):
        """Whether it is known if the person met the alternative residence requirements on July 1, 1977 as required by section 3(1)(b)(i) of the Old Age Security Act."""
        #       - All of:
        #         - did not reside in canada as of July 1, 1977
        #         - One of:
        #           - resided in canada for any period after 18 years of age as of July 1, 1977
        #           - possessed a valid immigration visa as of July 1, 1977
        not_resident_reversed = person("oas_s3_1_b_i_resided_in_canada", 1977_07_01)
        not_resident_known = not_(person("oas_s3_1_b_i_resided_in_canada_known", 1977_07_01))
        resided_after_18_or_visa = person("oas_s3_1_b_i_resided_in_canada_after_18_or_had_visa", 1977_07_01)
        resided_after_18_or_visa_known = person("oas_s3_1_b_i_resided_in_canada_after_18_or_had_visa_known", 1977_07_01)
        # A conjunction is known if any element is false or all are known.
        any_false = (not_resident_reversed * not_resident_known) + \
                    (not_(resided_after_18_or_visa) * resided_after_18_or_visa_known)
        all_known = not_resident_known * resided_after_18_or_visa_known
        return any_false + all_known

class oas_s3_1_b_i_resided_in_canada_after_18_or_had_visa(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the person had resided in Canada after age 18 or had a valid visa on July 1, 1977 as required by section 3(1)(b)(i) of the Old Age Security Act."

    def formula(person, period, parameters):
        """Whether the person had resided in Canada after age 18 or had a valid visaon July 1, 1977 as required by section 3(1)(b)(i) of the Old Age Security Act."""
        resided_after_18 = person("oas_s3_1_b_i_resided_in_canada_after_18", 1977_07_01)
        had_valid_visa = person("oas_s3_1_b_i_had_valid_visa", 1977_07_01)
        return resided_after_18 + had_valid_visa

class oas_s3_1_b_i_resided_in_canada_after_18_or_had_visa_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether it is known if the person had resided in Canada after age 18 or had a valid visa on July 1, 1977 as required by section 3(1)(b)(i) of the Old Age Security Act."

    def formula(person, period, parameters):
        """Whether it is known if the person had resided in Canada after age 18 or had a valid visaon July 1, 1977 as required by section 3(1)(b)(i) of the Old Age Security Act."""
        resided_after_18 = person("oas_s3_1_b_i_resided_in_canada_after_18", 1977_07_01)
        resided_after_18_known = person("oas_s3_1_b_i_resided_in_canada_after_18_known", 1977_07_01)
        had_valid_visa = person("oas_s3_1_b_i_had_valid_visa", 1977_07_01)
        had_valid_visa_known = person("oas_s3_1_b_i_had_valid_visa_known", 1977_07_01)
        # A disjunction is known if either is true or both are known
        any_true = (resided_after_18 * resided_after_18_known) + \
                    (had_valid_visa * had_valid_visa_known)
        all_known = resided_after_18_known * had_valid_visa_known
        return any_true + all_known

# We don't follow the usual naming convention here because this variable
# is reused in multiple paragraphs of s3(1).

class oas_s3_1_resided_in_canada_after_18(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the person had resided in Canada after age 18 on July 1, 1977 as required by section 3(1)(b)(i) and (c)(iii) of the Old Age Security Act."

class oas_s3_1_resided_in_canada_after_18(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether it is known if the person had resided in Canada after age 18 on July 1, 1977 as required by section 3(1)(b)(i) and (c)(iii) of the Old Age Security Act."

# It is questionable whether this shoud be modeled as a part of the section,
# or if it should be modeled somewhere else. But the question of whether or
# not a visa is "valid" is a legal conclusion, not something that can be known
# about the world without reference to the laws. So we include it as a legal
# variable, here, which represents the concept of "whether the person had
# a valid immigration visa for the purposes of section 3(1)(b)(i) of the Old
# Age Security Act".

class oas_s3_1_b_i_had_valid_visa(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the person had a valid visa on July 1, 1977 as required by section 3(1)(b)(i) of the Old Age Security Act."

class oas_s3_1_b_i_had_valid_visa_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the person had a valid visa on July 1, 1977 as required by section 3(1)(b)(i) of the Old Age Security Act."

# (c) every person who
# (i) was not a pensioner on July 1, 1977,
# (ii) has attained sixty-five years of age, and
# (iii) has resided in Canada after attaining eighteen years of age and prior to the day on which that person’s application is approved for an aggregate period of at least forty years.

class oas_s3_1_c_satisfied(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the person satisfies section 3(1)(c) of the Old Age Security Act."

    def formula(person, period, parameters):
        subi = person('oas_s3_1_c_i_satisfied', period)
        subii = person('oas_s3_1_c_ii_satisfied', period)
        subiii = person('oas_s3_1_c_iii_satisfied', period)
        return subi * subii * subiii

class oas_s3_1_c_satisfied_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether it is known if the person satisfies section 3(1)(c) of the Old Age Security Act."

    def formula(person, period, parameters):
        subi = person('oas_s3_1_c_i_satisfied', period)
        subi_known = person('oas_s3_1_c_i_satisfied_known', period)
        subii = person('oas_s3_1_c_ii_satisfied', period)
        subii_known = person('oas_s3_1_c_ii_satisfied_known', period)
        subiii = person('oas_s3_1_c_iii_satisfied', period)
        subiii_known = person('oas_s3_1_c_iii_satisfied_known', period)
        # A conjunction is known if any of its elements are known false, or all elements are known
        any_false = (not_(subi) * subi_known) + \
                    (not_(subii) * subii_known) + \
                    (not_(subiii) * subiii_known)
        all_known = subi_known * subii_known * subiii_known
        return any_false + all_known

# (i) was not a pensioner on July 1, 1977,

class oas_s3_1_c_i_satisfied(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the person satisfies section 3(1)(c)(i) of the Old Age Security Act."

    def formula(person, period, parameters):
        return not_(person('oas_s2_pensioner_satisfied',1977_07_01))

class oas_s3_1_c_i_satisfied_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether it is known if the person satisfies section 3(1)(c)(i) of the Old Age Security Act."

    def formula(person, period, parameters):
        return person('oas_s2_pensioner_satisfied_known',1977_07_01)

# (ii) has attained sixty-five years of age, and

class oas_s3_1_c_ii_satisfied(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the person satisfies section 3(1)(c)(ii) of the Old Age Security Act."

    def formula(person, period, parameters):
        return person('oas_s3_1_c_ii_at_minimum_age',period)

class oas_s3_1_c_ii_satisfied_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether it is known if the person satisfies section 3(1)(c)(ii) of the Old Age Security Act."

    def formula(person, period, parameters):
        return person('oas_s3_1_c_ii_at_minimum_age_known',period)


class oas_s3_1_c_ii_at_minimum_age(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the person is at or over the minimum age as required by section 3(1)(c)(ii) of the Old Age Security Act."

    def formula(person, period, parameters):
        return person('age',period) >= 65

class oas_s3_1_c_ii_at_minimum_age_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether it is known if the person is at or over the minimum age as required by section 3(1)(c)(ii) of the Old Age Security Act."

    def formula(person, period, parameters):
        return person('age_known',period)

# (iii) has resided in Canada after attaining eighteen years of age and
# prior to the day on which that person’s application is approved for an 
# aggregate period of at least forty years.

class oas_s3_1_c_iii_satisfied(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the person meets the requirements of section 3(1)(c)(iii) of the Old Age Security Act."

    def formula(person, period, parameters):
#TODO: Get rid of "resided" as a separate test, here, and in _known
        resided = person('oas_s3_1_resided_in_canada_after_18',period)
        approval_date = person('oas_s3_approval_date', period)
        resided_40_years = person('oas_s3_1_c_iii_resided_in_canada_40_years',approval_date.previous_day)
        return resided * resided_40_years

# Here is a problem I don't have an approach for, yet. What happens when multiple sections
# refer to identical concepts? Both (b) and (c) refer to the idea of residing in canada after
# age 18. Best practice is to re-use the concept, so I'm just re-using the first instance,
# but that is going to confuse explanations. So I think the better approach is to elevate
# the shared concept to the lowest level shared by all the parts that use it.
# in this case, oas_s3_1_b_i_resided_in_canada_after_18 would become oas_s3_1_resided_in_canada...

# So the question here is "will you have lived in Canada for 40 years as of
# the date prior to the date on which your applicaiton is approved."
# But the user cannot possibly
# know on what date their application will be approved. What we might be able
# to do is to offer them the ability to check on what date they will meet the
# requirements of section 3, by looking at various points in the future. But
# we can't really query that without creating a bunch of other variables for
# that purpose, or just querying it multiple times with different future dates.

class oas_s3_1_c_iii_satisfied_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the person meets the requirements of section 3(1)(c)(iii) of the Old Age Security Act."

    def formula(person, period, parameters):
        resided = person('oas_s3_1_resided_in_canada_after_18',period)
        resided_known = person('oas_s3_1_resided_in_canada_after_18_known',period)
        approval_date = person('oas_s3_approval_date', period)
        approval_date_known = person('oas_s3_approval_date_known', period)
        resided_40_years = person('oas_s3_1_c_iii_resided_in_canada_40_years',approval_date.previous_day)
        resided_40_years_known = person('oas_s3_1_c_iii_resided_in_canada_40_years_known',approval_date.previous_day)
        # A conjunction is known if any element is false or all are known.
        # in this case, the approval date is not conjoined, but it is used to calculate the other one.
        # The value of this is not known if using the current date doesn't return known true.
        # If the current date returns known true, then it will be true for all future dates.
        # This is a place where we are being forced to encode temporal constraints that should
        # be possible to make automatic.
        # We can't query "now" inside this formula, because we don't know what period it is being
        # asked to calculate about. We can ask whether as of the query date the person had
        # resided for 40 years, and whether the approval date was after today, but again that is
        # a sort of temporal constraint that is difficult to model in OpenFisca.

        any_false = (not_(resided) * resided_known) + \
                    (not_(resided_40_years) * resided_40_years_known)
        all_known = resided_known * resided_40_years_known * approval_date_known
        return any_false + all_known

class oas_s3_approval_date(Variable):
    value_type = date
    entity = Person
    definition_period = DAY
    label = "The date on which a person's application for OAS benefits is approved."

class oas_s3_approval_date_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "The date on which a person's application for OAS benefits is approved."
    
class oas_s3_1_c_iii_resided_in_canada_40_years(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the person has lived in Canada for 40 years in aggregate as required by section 3(1)(c)(iii) of the Old Age Security Act."

    # This is left as an input variable until and unless I decide to change the
    # way that place of residence inputs are requested. We could ask for a list
    # of places of residence and dates on which they were valid, and measure the time
    # between them. Or we could ask for a list of places the person has lived and how
    # long in each place. For now, we are asking yes or no, have you lived in Canada
    # for a total of 40 years.

class oas_s3_1_c_iii_resided_in_canada_40_years_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether it is known if the person has lived in Canada for 40 years in aggregate as required by section 3(1)(c)(iii) of the Old Age Security Act."

## Section 3(2)

# Payment of partial pension
# (2) Subject to this Act and the regulations, a partial monthly pension may be paid for any 
# month in a payment quarter to every person who is not eligible for a full monthly pension 
# under subsection (1) and
# (a) has attained sixty-five years of age; and
# (b) has resided in Canada after attaining eighteen years of age and prior to the day on 
# which that person’s application is approved for an aggregate period of at least ten years 
# but less than forty years and, where that aggregate period is less than twenty years, 
# was resident in Canada on the day preceding the day on which that person’s application 
# is approved.

# TO DO: We need to implement the time logic in this section more accurately. Need to know
# what a payment quarter is, and why it's referred to. Need to convert between things that
# change daily like ages, and things that are calculated with regard to months.

class oas_s3_2_satisfied(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "Whether a partial monthly pension may be paid under secton 3(2) of the Old Age Security Act."

    def formula(person, period, parameters):
        eligible_full_pension = person('oas_s3_1_satisfied', period)
        suba = person('oas_s3_2_a_satisfied', period)
        subb = person('oas_s3_2_b_satisfied', period)
        return not_(eligible_full_pension) * suba * subb

class oas_s3_2_satisfied_known(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "Whether it is known if a partial monthly pension may be paid under secton 3(2) of the Old Age Security Act."

    def formula(person, period, parameters):
        eligible_full_pension = person('oas_s3_1_satisfied', period)
        eligible_full_pension_known = person('oas_s3_1_satisfied_known', period)
        suba = person('oas_s3_2_a_satisfied', period)
        suba_known = person('oas_s3_2_a_satisfied_known', period)
        subb = person('oas_s3_2_b_satisfied', period)
        subb_known = person('oas_s3_2_b_satisfied_known', period)
        # A conjunction is known if any of its elements are false or all elements are known
        # In this case, one of the elements was being tested for falsehood, so we reverse that.
        any_false = (eligible_full_pension * eligible_full_pension_known) + \
                    (not_(suba) * suba_known) + (not_(subb) * subb_known)
        all_known = eligible_full_pension_known * suba_known * subb_known
        return any_false + all_known

# (a) has attained sixty-five years of age; and

class oas_s3_2_a_satisfied(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "Whether the person has reached the minimum age required in section 3(2)(a) of the Old Age Security Act."

    def formula(person, period, parameters):
        return person('oas_s3_2_a_minimum_age', period)

class oas_s3_2_a_satisfied_known(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "Whether it is known if the person has reached the minimum age required in section 3(2)(a) of the Old Age Security Act."

    def formula(person, period, parameters):
        return person('oas_s3_2_a_minimum_age_known', period)

class oas_s3_2_a_minimum_age(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "Whether the person is at least the minimum age for OAS eligibility."

    def formula(person, period, parameters):
        return person('age',period) >= 65 #need to parameterize this

class oas_s3_2_a_minimum_age_known(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "Whether the person is at least the minimum age for OAS eligibility."

    def formula(person, period, parameters):
        return person('age_known',period) >= 65 #need to parameterize this

# (b) has resided in Canada after attaining eighteen years of age and prior to the day on 
# which that person’s application is approved for an aggregate period of at least ten years 
# but less than forty years and, where that aggregate period is less than twenty years, 
# was resident in Canada on the day preceding the day on which that person’s application 
# is approved.

# Need to figure out how to do aggregate math, at this point, I think.

# Their residence is more than 20 years total, or more than 10 and they are resident on the
# day on which their application is approved.

class oas_s3_2_b_satisfied(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "Whether the person satisfies the requirements of s3(2)(b) of the Old Age Security Act."

    def formula(person, period, parameters):
        approval = person("oas_s3_approval_date",period)
        duration_minimum = person("oas_s3_2_b_minimum_duration",period)
        duration_maximum = person("oas_s3_2_b_maximum_duration",period)
        resident = person('oas_s3_2_b_residence',approval.previous_day)
        residence_required = person('oas_s3_2_b_residence_required',period)
        return duration_minimum * duration_maximum * \
            (not_(residence_required) + (residence_required * resident))

class oas_s3_2_b_satisfied_known(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "Whether it is known if the person satisfies the requirements of s3(2)(b) of the Old Age Security Act."

    def formula(person, period, parameters):
        approval = person("oas_s3_approval_date",period)
        approval_known = person("oas_s3_approval_date_known",period)
        duration_minimum = person("oas_s3_2_b_minimum_duration",period)
        duration_minimum_known = person("oas_s3_2_b_minimum_duration_known",period)
        duration_maximum = person("oas_s3_2_b_maximum_duration",period)
        duration_maximum_known = person("oas_s3_2_b_maximum_duration_known",period)
        resident = person('oas_s3_2_b_residence',approval.previous_day)
        resident_known = person('oas_s3_2_b_residence_known',approval.previous_day)
        residence_required = person('oas_s3_2_b_residence_required',period)
        residence_required_known = person('oas_s3_2_b_residence_required_known',period)
        # The sub-sub conjunction is known if any is known false or all are known.
        subsub_any_false = (not_(residence_required) * residence_required_known) + \
                            (not_(resident) * resident_known)
        subsub_all_known = residence_required_known * resident_known * approval_known
        subsub_known = subsub_any_false + subsub_all_known
        # The sub disjunction is known if any is known true, or all are known
        sub_any_true = (not_(residence_required) * residence_required_known) + \
                        (residence_required * resident * subsub_known)
        sub_all_known = residence_required_known * subsub_known
        sub_known = sub_any_true + sub_all_known
        # The main conjunction is known if any is known false, or all are known.
        any_false = (not_(duration_minimum) * duration_minimum_known) + \
                    (not_(duration_maximum) * duration_maximum_known) + \
                    (not_(not_(residence_required) + (residence_required * resident)) * sub_known)
        all_known = duration_minimum_known * duration_maximum_known * sub_known
        return any_false + all_known


class oas_s3_2_b_minimum_duration(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "Whether the person meets the minimum residence duration in s3(2)(b) of the Old Age Security Act."

    def formula(person, period, parameters):
        return person("oas_s3_duration_in_canada_since_18", period) >= 10

class oas_s3_2_b_minimum_duration_known(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "Whether it is known if the person meets the minimum residence duration in s3(2)(b) of the Old Age Security Act."

    def formula(person, period, parameters):
        return person("oas_s3_duration_in_canada_since_18_known", period)

class oas_s3_2_b_maximum_duration(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "Whether the person meets the maximum residence duration in s3(2)(b) of the Old Age Security Act."

    def formula(person, period, parameters):
        return person("oas_s3_duration_in_canada_since_18", period) < 40

class oas_s3_2_b_maximum_duration_known(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "Whether it is known if the person meets the maximum residence duration in s3(2)(b) of the Old Age Security Act."

    def formula(person, period, parameters):
        return person("oas_s3_duration_in_canada_since_18_known", period)

class oas_s3_2_b_residence_required(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "Whether the person must be resident in Canada to satisfy s3(2)(b) of the Old Age Security Act."

    def formula(person, period, parameters):
        return person("oas_s3_duration_in_canada_since_18", period) < 20

class oas_s3_2_b_residence_required_known (Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "Whether it is known if the person must be resident in Canada to satisfy s3(2)(b) of the Old Age Security Act."

    def formula(person, period, parameters):
        return person("oas_s3_duration_in_canada_since_18_known", period)


## Section 3(3) - (4)

# Amount of partial pension
# (3) Subject to subsection 7.1(3), the amount of a partial monthly pension, for any month, 
# shall bear the same relation to the amount of the full monthly pension for that month as the
#  aggregate period that the applicant has resided in Canada after attaining 18 years of age 
# and before the day on which the application is approved, determined in accordance with 
# subsection (4), bears to 40 years.

# The subject to section 7.1(3) part refers to a section that says a person is entitled to the
# largest of three calculations, one of which being this calculation. Because we are conlcuding
# the amount according to section 3(3) already, the part that is being overridden is just the
# absolute conclusion "the amount shall". We are not making a final conclusion about the amount.

class oas_s3_3_amount_of_partial_monthly_pension(Variable):
    value_type = float
    entity = Person
    definition_period = MONTH
    label = "The amount of the monthly partial pension set out in section 3(3) of the Old Age Security Act."

    def formula(person, period, parameters):
        ratio = person('oas_s3_3_ratio',period)
        full_monthly_pension = person('oas_XXX_full_monthly_pension', period) # I don't know where this is defined, yet.
        return full_monthly_pension * ratio

class oas_s3_3_amount_of_partial_monthly_pension_known(Variable):
    value_type = float
    entity = Person
    definition_period = MONTH
    label = "Whether we know the amount of the monthly partial pension set out in section 3(3) of the Old Age Security Act."

    def formula(person, period, parameters):
        ratio_known = person('oas_s3_3_ratio_known',period)
        full_monthly_pension_known = person('oas_XXX_full_monthly_pension_known', period) # I don't know where this is defined, yet.
        # This is not a conjunction, it it is an actual multiplcation. The result of a multiplication
        # is known if both the factors are known, and not othewrise.
        return full_monthly_pension_known * ratio_known

class oas_s3_3_ratio(Variable):
    value_type = float
    entity = Person
    definition_period = MONTH
    label = "The ratio applied to a full monthly pension to determine the partial monthly pension under section 3(3) of the Old Age Security Act."
    
    def formula(person, period, parameters):
        return person('oas_s3_4_duration',period) / 40

class oas_s3_3_ratio_known(Variable):
    value_type = float
    entity = Person
    definition_period = MONTH
    label = "The ratio applied to a full monthly pension to determine the partial monthly pension under section 3(3) of the Old Age Security Act."
    
    def formula(person, period, parameters):
        return person('oas_s3_4_duration_known',period)

# Rounding of aggregate period
# (4) For the purpose of calculating the amount of a partial monthly pension under 
# subsection (3), the aggregate period described in that subsection shall be rounded to the
#  lower multiple of a year when it is not a multiple of a year.

class oas_s3_4_duration(Variable):
    value_type = int
    entity = Person
    definition_period = MONTH
    label = "The number of years specified in s3(4) of the Old Age Security Act for calculating partial payment ratio."

    def formula(person, period, parameters):
        return floor(person('oas_s3_duration_in_canada_since_18',period))

class oas_s3_4_duration_known(Variable):
    value_type = int
    entity = Person
    definition_period = MONTH
    label = "Whether we know the number of years specified in s3(4) of the Old Age Security Act for calculating partial payment ratio."

    def formula(person, period, parameters):
        return person('oas_s3_duration_in_canada_since_18_known',period)



## Section 3(5)
#TODO: Implment section 3(5)
# Additional residence irrelevant for partial pensioner
# (5) Once a person’s application for a partial monthly pension has been approved, the
#  amount of monthly pension payable to that person under this Part may not be increased
#  on the basis of subsequent periods of residence in Canada.
#
# This section is super hard to encode. First, we need to model the event of approval. Then,
# we need to find a way to prohibit increases only, regardless of which other section of the law
# is calculating monthly pension payable, and prohibit increases only "on the basis of" subsequent
# periods of residence in Canada.
#
# So what we would need is something like:
# If the person has been approved for a partial monthly pension at a given amount, and
# If any variable in this code would calculate a higher amount after the time of the approval,
# and that variable would calculate a higher amount only because of an increase in the duration
# of time that has passed since the approval,
# then that section of code will instead conclude the approved amount.
#
# OpenFisca doesn't allow for such higher-order calculations. We will need to implement this as
# an additional rule when we do things like section 7.1(3), taking into account any approval dates
# in the past, or perhaps just asking for an input of previous approved amount.

