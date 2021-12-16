"""
This file defines variables for the modelled legislation.

A variable is a property of an Entity such as a Person, a Household…

See https://openfisca.org/doc/key-concepts/variables.html
"""

# Import from openfisca-core the Python objects used to code the legislation in OpenFisca
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

# Import the Entities specifically defined for this tax and benefit system
from openfisca_canada.entities import Household, Person

class oas_full_monthly_pension_payable(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "In accordance with section 3(1) of the Old Age Security Act, the person may be paid a full monthly pension."

    def formula(person, period, parameters):
        """Whether the person may, under section 3(1) of the Old Age Security Act, be paid a full monthly pension."""
        # Qualify under 3(1)(a),
        # QUalify under 3(1)(b), or
        # Qualify under 3(1)(c)
        return person("section_3_1_a_applies", period) * person("section_3_1_b_applies", period) * person("section_3_1_c_applies", period)

class section_3_1_a_applies(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "The person meets the definition of section 3(1)(a) of the Old Age Security Act."

    def formula(person, period, parameters):
        """Whether the person was, on July 1, 1977, a pensioner."""
        # every person who was a pensioner on July 1, 1977;
        return person("pensioner", 1977_07)

class section_3_1_b_applies(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "The person meeds the definition of section 3(1)(b) of the Old Age Security Act."

    def formula(person, period, parameters):
        """Whether the person is caught under section 3(1)(b) of the Old Age Security Act."""
        #Qualify under 3(1)(b)(i),
        #QUalify under 3(1)(b)(ii), and
        #Qualify under 3(1)(b)(iii)
        return person("section_3_1_b_i_applies", period) + person("section_3_1_b_ii_applies", period) + person("section_3_1_b_iii_applies", period)

class section_3_1_b_i_applies(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "The person meets the definition of section 3(1)(b)(i) of the Old Age Security Act."

    def formula(person, period, parameters):
        """Whether the person meets the definition of section 3(1)(b)(i) of the Old Age Security Act."""
        # Not a pensioner on July 1, 1977
        # On July 1, 1977 had attained 25 years of age and
            # On July 1, 1977 resided in Canada or
            # On July 1, 1977 did not reside in Canada and
                # On July 1, 1977 Had Resided in Canada for Any Period after Attaining 18 years of age, or
                # On July 1, 1977, possessed a valid immigration visa
        pensioner = person("pensioner", 1977_07)
        attained_25_yoa = person("age", 1977_07) > 25
        resided = person("country_of_residence", 1977_08) == "Canada"
        resided_after_18 = person("resided_in_canada_after_18_yoa", 1977_07)
        possessed_valid_visa = person("possessed_valid_immigration_visa", 1977_07)
        alternate_residence_requirement = (resided_after_18 + possessed_valid_visa) * not resided
        residence_requirement = resided
        age_and_residence = attained_25_yoa * (residence_requirement + alternate_residence_requirement)
        section = not pensioner * age_and_residence
        return section
