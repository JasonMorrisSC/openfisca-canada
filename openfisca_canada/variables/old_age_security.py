"""This is a module for calculating entitlement and eligibility for OAS benefits."""

from openfisca_core.indexed_enums import Enum
from openfisca_core.model_api import not_
from openfisca_core.periods import DAY, MONTH, YEAR
from openfisca_core.variables import Variable

from numpy import bool, float, int, isin, str, where

from openfisca_canada.entities import Person



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
        # Qualify under 3(1)(b)(i),
        # QUalify under 3(1)(b)(ii), and
        # Qualify under 3(1)(b)(iii)
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
        alternate_residence_requirement = (resided_after_18 + possessed_valid_visa) * not_(resided)
        residence_requirement = resided
        age_and_residence = attained_25_yoa * (residence_requirement + alternate_residence_requirement)
        section = not pensioner * age_and_residence
        return section


class age_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether we know the Person's age"


class place_of_residence(Variable):
    value_type = str
    entity = Person
    definition_period = DAY
    label = "Person's place of residence, expressed as a 2 letter ISO-3166-1 code"


class place_of_residence_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether Person's place of residence is known"


class legal_status_options(Enum):
    CANADIAN_CITIZEN = u"CANADIAN_CITIZEN"
    PERMANENT_RESIDENT = u"PERMANENT_RESIDENT",
    STATUS_INDIAN = u"STATUS_INDIAN",
    TEMPORARY_RESIDENT = u"TEMPORARY_RESIDENT",
    OTHER = u"OTHER"


class legal_status(Variable):
    value_type = Enum
    possible_values = legal_status_options
    default_value = legal_status_options.OTHER
    entity = Person
    definition_period = DAY
    label = "Person's legal status in Canada"


class legal_status_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether we know the Person's legal status in Canada"


class years_in_canada_since_18(Variable):
    value_type = int
    entity = Person
    definition_period = DAY
    label = "Person's aggregate years lived in Canada"


class years_in_canada_since_18_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether we know the Person's aggregate years lived in Canada"


class marital_status_options(Enum):
    SINGLE = u"Single",
    MARRIED = u"Married",
    COMMONLAW = u"Common-law",
    WIDOWED = u"Widowed",
    DIVORCED = u"Divorced",
    SEPERATED = u"Seperated"


class marital_status(Variable):
    value_type = Enum
    possible_values = marital_status_options
    default_value = marital_status_options.SINGLE
    entity = Person
    definition_period = DAY
    label = "Person's marital status"


class marital_status_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether we know the Person's marital status"


class partner_receiving_oas(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether Person's partner is receiving OAS"


class partner_receiving_oas_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether we know if the Person's partner is receiving OAS"


class income(Variable):
    value_type = int
    entity = Person
    definition_period = YEAR
    label = "Person's annual income"


class income_known(Variable):
    value_type = bool
    entity = Person
    definition_period = YEAR
    label = "Whether we know the Person's annual income"


class eligible_under_social_agreement(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether Person is eligible under the social agreement between Canada and their place of residence"


class eligible_under_social_agreement_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether we know if the Person is eligible under the social agreement between Canada and their place of residence"


class resides_in_agreement_country(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether Person's place of residence has a social agreement with Canada"

    def formula(person, period, parameters):
        """Whether Person's place of residence has a social agreement with Canada."""
        # The person's country of residence is valid if they were on the list of countries with which Canada had
        # agreements at the time. That will be created as a parameter, so it can vary by date.
        return isin(person("place_of_residence", period), parameters(period).benefits.social_agreement_countries)


class resides_in_agreement_country_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether we know if the Person's place of residence has a social agreement with Canada"

    def formula(person, period, parameters):
        """Whether we know if the Person's place of residence has a social agreement with Canada."""
        return person("place_of_residence_known", period)


class resided_in_agreement_country(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the Person's place of residence has ever been in a country with a social agreement with Canada"


class resided_in_agreement_country_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether it is known whether the person's place of residence has ever been in a country with a social agreement with Canada"


class oas_eligible(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether Person is eligible for OAS"

    def formula(person, period, parameters):
        """Whether Person is eligible for OAS."""
        return person("oas_eligible_income_requirement_satisfied", period) * person("oas_eligible_age_requirement_satisfied", period) * person("oas_eligible_legal_status_satisfied", period) * person("oas_eligible_required_residency_duration_satisfied", period) \
            * person("oas_eligible_residency_requirement_satisfied", period)


class oas_eligible_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the Person's eligibility for OAS is known"

    def formula(person, period, parameters):
        """Whether the Person's eligibility for OAS is known."""
        # The answer to a conjunction is known if a) all of the conclusions are known,
        # or b) if any of the conclusions is known to be false.
        all_true = person("oas_eligible_income_requirement_satisfied_known", period) * person("oas_eligible_age_requirement_satisfied_known", period) * person("oas_eligible_legal_status_satisfied_known", period) * person("oas_eligible_required_residency_duration_satisfied_known", period) \
            * person("oas_eligible_residency_requirement_satisfied_known", period)
        income_false = person("oas_eligible_income_requirement_satisfied_known", period) * not_(person("oas_eligible_income_requirement_satisfied", period))
        age_false = person("oas_eligible_age_requirement_satisfied_known", period) * not_(person("oas_eligible_age_requirement_satisfied", period))
        legal_status_false = person("oas_eligible_legal_status_satisfied_known", period) * not_(person("oas_eligible_legal_status_satisfied_known", period))
        residency_duration_false = person("oas_eligible_required_residency_duration_satisfied_known", period) * not_(person("oas_eligible_required_residency_duration_satisfied", period))
        residency_false = person("oas_eligible_residency_requirement_satisfied_known", period) * not_(person("oas_eligible_residency_requirement_satisfied", period))
        any_false = income_false + age_false + legal_status_false + residency_duration_false + residency_false
        return all_true + any_false


class oas_eligible_required_residency_duration_amount(Variable):
    value_type = int
    entity = Person
    definition_period = DAY
    label = "How many years the person is required to have resided in Canada to qualify for OAS"

    def formula(person, period, parameters):
        """How many years the person is required to have resided in Canada to qualify for OAS."""
        required_years = where(person("place_of_residence", period) == "CA", 10, 20)
        return required_years


class oas_eligible_required_residency_duration_amount_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether we know how many years the person is required to have resided in Canada to qualify for OAS"

    def formula(person, period, parameters):
        """Whether we know how many years the person is required to have resided in Canada to qualify for OAS."""
        known = person("place_of_residence_known", period)
        return known


class oas_eligible_required_residency_duration_satisfied(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the person has resided in Canada long enough to qualify for OAS"

    def formula(person, period, parameters):
        """Whether the person has resided in Canada long enough to qualify for OAS."""
        return person("years_in_canada_since_18", period) >= person("oas_eligible_required_residency_duration_amount", period)


class oas_eligible_required_residency_duration_satisfied_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether we know if the person has resided in Canada long enough to qualify for OAS"

    def formula(person, period, parameters):
        """Whether we know if the person has resided in Canada long enough to qualify for OAS."""
        return person("years_in_canada_since_18_known", period) * person("oas_eligible_required_residency_duration_amount_known", period)


class oas_eligible_legal_status_satisfied(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the person has the required legal status in Canada for OAS eligibility"

    def formula(person, period, parameters):
        """Whether the person has the required legal status in Canada for OAS eligibility."""
        satisfied = person("oas_eligible_legal_status__qualifies", period)
        return satisfied


class oas_eligible_legal_status_satisfied_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether we know if the person has the required legal status in Canada for OAS eligibility"

    def formula(person, period, parameters):
        """Whether we know if the person has the required legal status in Canada for OAS eligibility."""
        known = person("oas_eligible_legal_status__qualifies_known", period)
        return known


class oas_eligible_legal_status__qualifies(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the person has one of the four qualifying legal status for OAS Eligibility"

    def formula(person, period, parameters):
        """Whether the person has one of the four qualifying legal status for OAS Eligibility."""
        citizen = person("legal_status", period) == legal_status_options.CANADIAN_CITIZEN
        indian = person("legal_status", period) == legal_status_options.STATUS_INDIAN
        perm = person("legal_status", period) == legal_status_options.PERMANENT_RESIDENT
        temp = person("legal_status", period) == legal_status_options.TEMPORARY_RESIDENT
        return citizen + indian + perm + temp


class oas_eligible_legal_status__qualifies_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether we know if the person has one of the four qualifying legal status for OAS Eligibility"

    def formula(person, period, parameters):
        """Whether we know if the person has one of the four qualifying legal status for OAS Eligibility."""
        return person("legal_status_known", period)


class oas_eligible_residency_requirement_satisfied(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the residency requirement for OAS is satisfied by the Person"

    def formula(person, period, parameters):
        """Whether the residency requirement for OAS is satisfied by the Person."""
        satisfied = person("oas_eligible_canadian_residency_requirement_satisfied", period) + person("oas_eligible_foreign_residency_requirement_satisfied", period)
        return satisfied


class oas_eligible_residency_requirement_satisfied_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether we know if the residency requirement for OAS is satisfied by the Person"

    def formula(person, period, parameters):
        """Whether we know if the residency requirement for OAS is satisfied by the Person."""
        # A disjunction is known if all of the components are known, or if any of
        # the components is known and true.
        canadian_true = person("oas_eligible_canadian_residency_requirement_satisfied_known", period) * person("oas_eligible_canadian_residency_requirement_satisfied", period)
        foreign_true = person("oas_eligible_foreign_residency_requirement_satisfied_known", period) * person("oas_eligible_foreign_residency_requirement_satisfied", period)
        all_known = person("oas_eligible_canadian_residency_requirement_satisfied_known", period) * person("oas_eligible_foreign_residency_requirement_satisfied_known", period)
        one_true = canadian_true + foreign_true
        known = one_true + all_known
        return known


class oas_eligible_canadian_residency_requirement_satisfied(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the Person satisfies the canadian residency option of the residency requirement for Old Age Security"

    def formula(person, period, parameters):
        """Whether the Person satisfies the canadian residency option of the residency requirement for Old Age Security."""
        return person("place_of_residence", period) == "CA"


class oas_eligible_canadian_residency_requirement_satisfied_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether we know if the Person satisfies the canadian residency option of the residency requirement for Old Age Security"

    def formula(person, period, parameters):
        """Whether we know if the Person satisfies the canadian residency option of the residency requirement for Old Age Security."""
        return person("place_of_residence_known", period)


class oas_eligible_foreign_residency_requirement_satisfied(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the person satisfies the foreign residency option of the residency requirement for Old Age Security"

    def formula(person, period, parameters):
        """Whether the person satisfies the foreign residency option of the residency requirement for Old Age Security."""
        return person("resides_in_agreement_country", period) * person("eligible_under_social_agreement", period)


class oas_eligible_foreign_residency_requirement_satisfied_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether we know if the person satisfies the foreign residency option of the residency requirement for Old Age Security"

    def formula(person, period, parameters):
        """Whether we know if the person satisfies the foreign residency option of the residency requirement for Old Age Security."""
        # A conjunction is known if one of its elements is known false, or if all of its elements are known.
        not_resides_in_country = person("resides_in_agreement_country_known", period) * not_(person("resides_in_agreement_country", period))
        not_eligible = person("eligible_under_social_agreement_known", period) * not_(person("eligible_under_social_agreement", period))
        one_false = not_resides_in_country + not_eligible
        all_known = person("resides_in_agreement_country_known", period) * person("eligible_under_social_agreement_known", period)
        return all_known + one_false


class oas_eligible_income_requirement_satisfied(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the income requirement for OAS is satisfied"

    def formula(person, period, parameters):
        """Whether the income requirement for OAS is satisfied."""
        satisfied = person("oas_eligible__income_not_above_limit", period)
        return satisfied


class oas_eligible_income_requirement_satisfied_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether we know if the income requirement for OAS is satisfied"

    def formula(person, period, parameters):
        """Whether we know if the income requirement for OAS is satisfied."""
        known = person("oas_eligible__income_not_above_limit_known", period)
        return known


class oas_eligible__income_not_above_limit(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the peron's income is not above the limit for OAS eligibility"

    def formula(person, period, parameters):
        """Whether the peron's income is not above the limit for OAS eligibility."""
        not_income_too_high = not_(person("income", period.this_year) > parameters(period).benefits.old_age_security.max_income)
        return not_income_too_high


class oas_eligible__income_not_above_limit_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether we know if the peron's income is not above the limit for OAS eligibility"

    def formula(person, period, parameters):
        """Whether we know if the peron's income is not above the limit for OAS eligibility."""
        known = person("income_known", period.this_year)
        return known


class oas_eligible_age_requirement_satisfied(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the age requirement for OAS is satisfied"

    def formula(person, period, parameters):
        """Whether the age requirement for OAS is satisfied."""
        satisfied = person("oas_eligible__age_above_eligibility", period)
        return satisfied


class oas_eligible_age_requirement_satisfied_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether we know if the age requirement for OAS is satisfied"

    def formula(person, period, parameters):
        """Whether we know if the age requirement for OAS is satisfied."""
        known = person("oas_eligible__age_above_eligibility_known", period)
        return known


class oas_eligible__age_above_eligibility(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the person's age is above the OAS age minimum for eligibility"

    def formula(person, period, parameters):
        """Whether the person's age is above the OAS age minimum for eligibility."""
        age_requirement_met = person("age", period) >= parameters(period).benefits.old_age_security.eligibility_age
        return age_requirement_met


class oas_eligible__age_above_eligibility_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether we know if the person's age is above the OAS age minimum for eligibility"

    def formula(person, period, parameters):
        """Whether we know if the person's age is above the OAS age minimum for eligibility."""
        known = person("age_known", period)
        return known


class gis_eligible(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether Person is eligible for Guaranteed Income Supplement"

    def formula(person, period, parameters):
        """Whether Person is eligible for Guaranteed Income Supplement."""
        return person("oas_eligible", period) * person("gis_eligible_income", period) * person("gis_eligible_age", period)


class gis_eligible_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether it is known if the Person is eligible for Guaranteed Income Supplement"

    def formula(person, period, parameters):
        """Whether it is known if the Person is eligible for Guaranteed Income Supplement."""
        all_known = person("oas_eligible_known", period) * person("gis_eligible_income_known", period) * person("gis_eligible_age_known", period)
        oas_false = person("oas_eligible_known", period) * not_(person("oas_eligible", period))
        income_false = person("gis_eligible_income_known", period) * not_(person("gis_eligible_income", period))
        age_false = person("gis_eligible_age_known", period) * person("gis_eligible_age", period)
        any_false = oas_false + income_false + age_false
        return any_false + all_known


class gis_eligible_age(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the person's age meets the requirements for Guaranteed Income Supplement"

    def formula(person, period, parameters):
        """Whether the person's age meets the requirements for Guaranteed Income Supplement."""
        return person("age", period) >= parameters(period).benefits.old_age_security.eligibility_age


class gis_eligible_age_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether we know if the person's age meets the requirements for Guaranteed Income Supplement"

    def formula(person, period, parameters):
        """Whether we know if the person's age meets the requirements for Guaranteed Income Supplement."""
        return person("age_known", period)


class gis_eligible_income(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the person's income meets the requirements for Guaranteed Income Supplement"

    def formula(person, period, parameters):
        """Whether the person's income meets the requirements for Guaranteed Income Supplement."""
        income_requirement = person("income", period.this_year) < person("gis_eligible_income_max", period)
        return income_requirement


class gis_eligible_income_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether we know if the person's income meets the requirements for Guaranteed Income Supplement"

    def formula(person, period, parameters):
        """Whether we know if the person's income meets the requirements for Guaranteed Income Supplement."""
        return person("income_known", period.this_year) * person("gis_eligible_income_max_known", period)


class gis_eligible_income_max(Variable):
    value_type = int
    entity = Person
    definition_period = DAY
    label = "The person's maximum income for GIS eligibility"

    def formula(person, period, parameters):
        """The person's maximum income for GIS eligibility."""
        max_single = parameters(period).benefits.old_age_security.guaranteed_income_supplement.maximum_income_single
        max_partner = parameters(period).benefits.old_age_security.guaranteed_income_supplement.maximum_income_partnered
        max_both = parameters(period).benefits.old_age_security.guaranteed_income_supplement.maximum_income_two_recipients

        max_income = where(person("gis_eligible_income_max_partnered", period), max_partner, max_single)
        max_income = where(person("partner_receiving_oas", period), max_both, max_income)
        return max_income


class gis_eligible_income_max_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether we know the person's maximum income for GIS eligibility"

    def formula(person, period, parameters):
        """Whether we know the person's maximum income for GIS eligibility."""
        # The max is known if the person is not partnered, or if their marital status and partner receiving is known

        not_partnered = not_(person("gis_eligible_income_max_partnered", period)) * person("gis_eligible_income_max_partnered_known", period)
        both_known = person("marital_status_known", period) * person("partner_receiving_oas_known", period)
        return not_partnered + both_known


class gis_eligible_income_max_partnered(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the person has a partner for GIS eligibility"

    def formula(person, period, parameters):
        """Whether the person has a partner for GIS eligibility."""
        married = person("marital_status", period) == marital_status_options.MARRIED
        common_law = person("marital_status", period) == marital_status_options.COMMONLAW
        return married + common_law


class gis_eligible_income_max_partnered_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether we know if the person has a partner for GIS eligibility"

    def formula(person, period, parameters):
        """Whether we know if the person has a partner for GIS eligibility."""
        return person("marital_status_known", period)

# class gis_eligible_reason(Variable):
#     value_type = str
#     entity = Person
#     definition_period = DAY
#     label = "Why the Person is or is not eligible for Guaranteed Income Supplement"

#     def formula(person, period, parameters):
#         married = person("marital_status",period) == marital_status_options.MARRIED
#         common_law = person("marital_status",period) == marital_status_options.COMMONLAW
#         partnered = married + common_law
#         max_single = parameters(period).benefits.old_age_security.guaranteed_income_supplement.maximum_income_single
#         max_partner = parameters(period).benefits.old_age_security.guaranteed_income_supplement.maximum_income_partnered
#         max_both = parameters(period).benefits.old_age_security.guaranteed_income_supplement.maximum_income_two_recipients

#         max_income = where(partnered,max_partner,max_single)
#         max_income = where(person("partner_receiving_oas",period),max_both,max_income)
#         income_requirement = person("income",period.this_year) < max_income
#         age_requirement = person("age",period) >= parameters(period).benefits.old_age_security.eligibility_age

#         reason = where(person("oas_eligible",period) * income_requirement * age_requirement, "You appear to be eligible for the Guaranteed Income Supplement.","")
#         reason = where(not_(age_requirement),"You must be 65 years of age to be eligible for the Guaranteed Income Supplement.",reason)
#         reason = where(not_(income_requirement),"You make too much money to be eligible for the Guaranteed Income Supplement.",reason)
#         reason = where(not_(person("oas_eligible",period)),"You must be eligible for Old Age Security to be eligible for the Guaranteed Income Supplement.",reason)

#         return reason


class allowance_eligible(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether Person is eligible for allowance"

    def formula(person, period, parameters):
        """Whether Person is eligible for allowance."""
        residence_requirement = person("allowance_residence_requirement_satisfied", period)
        partnered_requirement = person("allowance_partnered_requirement_satisfied", period)
        partner_receiving_requirement = person("allowance_partner_receiving_requirement_satisfied", period)
        income_requirement = person("allowance_income_requirement_satisfied", period)
        age_requirement = person("allowance_age_requirement_satisfied", period)
        return residence_requirement * partnered_requirement * partner_receiving_requirement * income_requirement * age_requirement


class allowance_eligible_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether it is known if Person is eligible for Allowance"

    def formula(person, period, parameters):
        """Whether it is known if Person is eligible for Allowance."""
        # A conjunction is known if any part is known false, or all parts are known
        age_false = person("allowance_age_requirement_satisfied_known", period) * not_(person("allowance_age_requirement_satisfied", period))
        partnered_false = person("allowance_partnered_requirement_satisfied_known", period) * not_(person("allowance_partnered_requirement_satisfied", period))
        partner_receiving_false = person("allowance_partner_receiving_requirement_satisfied_known", period) * not_(person("allowance_partner_receiving_requirement_satisfied", period))
        income_false = person("allowance_income_requirement_satisfied_known", period) * not_(person("allowance_income_requirement_satisfied", period))
        residence_false = person("allowance_residence_requirement_satisfied_known", period) * not_(person("allowance_residence_requirement_satisfied", period))
        any_false = age_false + partnered_false + income_false + residence_false + partner_receiving_false
        all_known = person("allowance_age_requirement_satisfied_known", period) * person("allowance_partnered_requirement_satisfied_known", period) * person("allowance_income_requirement_satisfied_known", period) * person("allowance_residence_requirement_satisfied_known", period) * person("allowance_partner_receiving_requirement_satisfied_known", period)
        return any_false + all_known


class allowance_residence_requirement_satisfied(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the person meets the residence requirements for Allowance eligibility"

    def formula(person, period, parameters):
        """Whether the person meets the residence requirements for Allowance eligibility."""
        return person("allowance_residence_canadian_satisfied", period) + person("allowance_residence_foreign_satisfied", period)


class allowance_residence_requirement_satisfied_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the person meets the residence requirements for Allowance eligibility"

    def formula(person, period, parameters):
        """Whether the person meets the residence requirements for Allowance eligibility."""
        # A disjunction is known if either is known true, or both are known
        canadian_true = person("allowance_residence_canadian_satisfied_known", period) * person("allowance_residence_canadian_satisfied", period)
        foreign_true = person("allowance_residence_foreign_satisfied_known", period) * person("allowance_residence_foreign_satisfied", period)
        either_true = canadian_true + foreign_true
        both_known = person("allowance_residence_canadian_satisfied_known", period) * person("allowance_residence_foreign_satisfied_known", period)
        return either_true + both_known


class allowance_residence_canadian_satisfied(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the person meets the Canadian residence requirements for Allowance eligibility"

    def formula(person, period, parameters):
        """Whether the person meets the Canadian residence requirements for Allowance eligibility."""
        return person("allowance_residence_canadian_status_satisfied", period) * person("allowance_residence_duration_satisfied", period)


class allowance_residence_canadian_satisfied_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether it is known if the person meets the Canadian residence requirements for Allowance eligibility"

    def formula(person, period, parameters):
        """Whether it is known if the person meets the Canadian residence requirements for Allowance eligibility."""
        # A conjunction is known if either is known false or both are known
        canadian_false = person("allowance_residence_canadian_status_satisfied_known", period) * not_(person("allowance_residence_canadian_status_satisfied", period))
        duration_false = person("allowance_residence_duration_satisfied_known", period) * not_(person("allowance_residence_duration_satisfied", period))
        either_false = canadian_false + duration_false
        both_known = person("allowance_residence_canadian_status_satisfied_known", period) * person("allowance_residence_duration_satisfied_known", period)
        return either_false + both_known


class allowance_residence_canadian_status_satisfied(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the person meets the residence requirements for Allowance eligibility"

    def formula(person, period, parameters):
        """Whether the person meets the residence requirements for Allowance eligibility."""
        citizen = person("legal_status", period) == legal_status_options.CANADIAN_CITIZEN
        indian = person("legal_status", period) == legal_status_options.STATUS_INDIAN
        perm = person("legal_status", period) == legal_status_options.PERMANENT_RESIDENT
        temp = person("legal_status", period) == legal_status_options.TEMPORARY_RESIDENT
        return citizen + indian + perm + temp


class allowance_residence_canadian_status_satisfied_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether it is known if the person meets the residence requirements for Allowance eligibility"

    def formula(person, period, parameters):
        """Whether it is known if the person meets the residence requirements for Allowance eligibility."""
        return person("legal_status_known", period)


class allowance_residence_duration_satisfied(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the person meets the residence requirements for Allowance eligibility"

    def formula(person, period, parameters):
        """Whether the person meets the residence requirements for Allowance eligibility."""
        minimum_years = parameters(period).benefits.old_age_security.allowance.minimum_years
        return person("years_in_canada_since_18", period) >= minimum_years


class allowance_residence_duration_satisfied_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether we know if the person meets the residence requirements for Allowance eligibility"

    def formula(person, period, parameters):
        """Whether we know if the person meets the residence requirements for Allowance eligibility."""
        return person("years_in_canada_since_18_known", period)


class allowance_residence_foreign_satisfied(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the person meets the foreign residence requirements for Allowance eligibility"

    def formula(person, period, parameters):
        """Whether the person meets the foreign residence requirements for Allowance eligibility."""
        return person("allowance_residence_foreign_in_agreement_country_satisfied", period) * person("allowance_residence_foreign_qualified_satisfied", period) * person("allowance_residence_duration_satisfied", period)


class allowance_residence_foreign_satisfied_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether it is known if the person meets the foreign residence requirements for Allowance eligibility"

    def formula(person, period, parameters):
        """Whether it is known if the person meets the foreign residence requirements for Allowance eligibility."""
        # Conjunctions are known if any are known false or all are known.
        in_agreement_false = person("allowance_residence_foreign_in_agreement_country_satisfied_known", period) * not_(person("allowance_residence_foreign_in_agreement_country_satisfied", period))
        qualified_false = person("allowance_residence_foreign_qualified_satisfied_known", period) * not_(person("allowance_residence_foreign_qualified_satisfied", period))
        duration_false = person("allowance_residence_duration_satisfied_known", period) * not_(person("allowance_residence_duration_satisfied", period))
        any_false = in_agreement_false + qualified_false + duration_false
        all_known = person("allowance_residence_foreign_in_agreement_country_satisfied_known", period) * person("allowance_residence_foreign_qualified_satisfied_known", period) * person("allowance_residence_duration_satisfied_known", period)
        return any_false + all_known


class allowance_residence_foreign_in_agreement_country_satisfied(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the person meets the foreign residence requirements for Allowance eligibility"

    def formula(person, period, parameters):
        """Whether the person meets the foreign residence requirements for Allowance eligibility."""
        return person("resides_in_agreement_country", period)


class allowance_residence_foreign_in_agreement_country_satisfied_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether it is known if the person meets the foreign residence requirements for Allowance eligibility"

    def formula(person, period, parameters):
        """Whether it is known if the person meets the foreign residence requirements for Allowance eligibility."""
        return person("resides_in_agreement_country_known", period)


class allowance_residence_foreign_qualified_satisfied(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the person meets the foreign residence requirements for Allowance eligibility"

    def formula(person, period, parameters):
        """Whether the person meets the foreign residence requirements for Allowance eligibility."""
        return person("eligible_under_social_agreement", period)


class allowance_residence_foreign_qualified_satisfied_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether it is known if the person meets the foreign residence requirements for Allowance eligibility"

    def formula(person, period, parameters):
        """Whether it is known if the person meets the foreign residence requirements for Allowance eligibility."""
        return person("eligible_under_social_agreement_known", period)


class allowance_partnered_requirement_satisfied(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the required of being partnered is satisfied for Allowance eligibility"

    def formula(person, period, parameters):
        """Whether the required of being partnered is satisfied for Allowance eligibility."""
        married = person("marital_status", period) == marital_status_options.MARRIED
        common_law = person("marital_status", period) == marital_status_options.COMMONLAW
        return married + common_law


class allowance_partnered_requirement_satisfied_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether we know if the required of being partnered is satisfied for Allowance eligibility"

    def formula(person, period, parameters):
        """Whether we know if the required of being partnered is satisfied for Allowance eligibility."""
        married_true = (person("marital_status", period) == marital_status_options.MARRIED) * person("marital_status_known", period)
        common_law_true = (person("marital_status", period) == marital_status_options.COMMONLAW) * person("marital_status_known", period)
        either_true = married_true + common_law_true
        both_known = person("marital_status_known", period)
        return either_true + both_known


class allowance_partner_receiving_requirement_satisfied(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the requirement for Allowance that the partner be receiving OAS is satisfied"

    def formula(person, period, parameters):
        """Whether the requirement for Allowance that the partner be receiving OAS is satisfied."""
        return person("partner_receiving_oas", period)


class allowance_partner_receiving_requirement_satisfied_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether it is known if the requirement for Allowance that the partner be receiving OAS is satisfied"

    def formula(person, period, parameters):
        """Whether it is known if the requirement for Allowance that the partner be receiving OAS is satisfied."""
        return person("partner_receiving_oas_known", period)


class allowance_income_requirement_satisfied(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the person's income meets the requirement for allowance"

    def formula(person, period, parameters):
        """Whether the person's income meets the requirement for allowance."""
        income_cap = parameters(period).benefits.old_age_security.allowance.income_cap
        income_requirement = person("income", period.this_year) < income_cap
        return income_requirement


class allowance_income_requirement_satisfied_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether it is known if the person's income meets the requirement for allowance"

    def formula(person, period, parameters):
        """Whether it is known if the person's income meets the requirement for allowance."""
        return person("income_known", period.this_year)


class allowance_age_requirement_satisfied(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the age requirement is satisfied for Allowance eligibility"

    def formula(person, period, parameters):
        """Whether the age requirement is satisfied for Allowance eligibility."""
        return person("allowance_age_requirement_minimum_satisfied", period) * person("allowance_age_requirement_cap_satisfied", period)


class allowance_age_requirement_satisfied_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether it is known if the age requirement is satisfied for Allowance eligibility"

    def formula(person, period, parameters):
        """Whether it is known if the age requirement is satisfied for Allowance eligibility."""
        # A conjunction is known if all the elements are known or any element in known false.
        min_false = person("allowance_age_requirement_minimum_satisfied_known", period) * not_(person("allowance_age_requirement_minimum_satisfied", period))
        cap_false = person("allowance_age_requirement_cap_satisfied_known", period) * not_(person("allowance_age_requirement_cap_satisfied", period))
        any_false = min_false + cap_false
        all_known = person("allowance_age_requirement_minimum_satisfied_known", period) * person("allowance_age_requirement_cap_satisfied_known", period)
        return any_false + all_known


class allowance_age_requirement_minimum_satisfied(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the minimum age requirement is satisfied for Allowance eligibility"

    def formula(person, period, parameters):
        """Whether the minimum age requirement is satisfied for Allowance eligibility."""
        minimum_age = parameters(period).benefits.old_age_security.allowance.minimum_age
        return person("age", period) >= minimum_age


class allowance_age_requirement_minimum_satisfied_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether it is known if the minimum age requirement is satisfied for Allowance eligibility"

    def formula(person, period, parameters):
        """Whether it is known if the minimum age requirement is satisfied for Allowance eligibility."""
        return person("age_known", period)


class allowance_age_requirement_cap_satisfied(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the maximum age requirement is satisfied for Allowance eligibility"

    def formula(person, period, parameters):
        """Whether the maximum age requirement is satisfied for Allowance eligibility."""
        cap = parameters(period).benefits.old_age_security.eligibility_age
        return person("age", period) < cap


class allowance_age_requirement_cap_satisfied_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether it is known if the maximum age requirement is satisfied for Allowance eligibility"

    def formula(person, period, parameters):
        """Whether it is known if the maximum age requirement is satisfied for Allowance eligibility."""
        return person("age_known", period)


# class allowance_eligible_reason(Variable):
#     value_type = str
#     entity = Person
#     definition_period = DAY
#     label = "Whether Person is eligible for allowance"

#     def formula(person, period, parameters):
#         citizen = person("legal_status",period) == legal_status_options.CANADIAN_CITIZEN
#         indian = person("legal_status",period) == legal_status_options.STATUS_INDIAN
#         perm = person("legal_status",period) == legal_status_options.PERMANENT_RESIDENT
#         temp = person("legal_status",period) == legal_status_options.TEMPORARY_RESIDENT
#         canadian_resident = citizen + indian + perm + temp
#         married = person("marital_status",period) == marital_status_options.MARRIED
#         common_law = person("marital_status",period) == marital_status_options.COMMONLAW
#         partnered_requirement = married + common_law
#         minimum_years = parameters(period).benefits.old_age_security.allowance.minimum_years
#         in_country_with_agreement = person("resides_in_agreement_country",period)
#         minimum_age = parameters(period).benefits.old_age_security.allowance.minimum_age
#         # Note that we are making an assumption that the minimum age for OAS and the
#         # age cap for the allowance will always be the same value.
#         age_cap = parameters(period).benefits.old_age_security.eligibility_age
#         income_cap = parameters(period).benefits.old_age_security.allowance.income_cap
#         age = person("age",period)
#         age_requirement = (age >= minimum_age) * (age < age_cap)
#         income_requirement = person("income",period.this_year) < income_cap
#         partner_receiving_requirement = person("partner_receiving_oas",period)
#         years_in_canada = person("years_in_canada_since_18", period)
#         canadian_residence_requirement = canadian_resident * (years_in_canada >= minimum_years)
#         eligible_under_social_agreement = person("eligible_under_social_agreement",period)
#         alternative_residence_requirement = in_country_with_agreement * eligible_under_social_agreement * (years_in_canada >= minimum_years)
#         residence_requirement = canadian_residence_requirement + alternative_residence_requirement

#         # This is a different approach to the reasons that returns only one reason, not multiple.
#         # Note that which reason gets displayed is dependent on the order of the lines
#         # of code below.
#         reason = where(residence_requirement * partnered_requirement * partner_receiving_requirement * income_requirement * age_requirement, "Based on the information provided, you are eligible for Allowance!", "")
#         reason = where(not_(age_requirement),"You must be between 60 and 64 to be eligible for Allowance",reason)
#         reason = where(not_(income_requirement), "Your income is too high to be eligible for Allowance",reason)
#         reason = where(not_(partnered_requirement), "You must be common-law or married to be eligible for Allowance", reason)
#         reason = where(not_(partner_receiving_requirement), "Your partner must be receiving OAS to be eligible for Allowance", reason)
#         reason = where(not_(years_in_canada >= minimum_years), "You must have lived in Canada for at least 10 years to be eligible for Allowance", reason)
#         reason = where(not_(canadian_residence_requirement + alternative_residence_requirement), "You must either live in Canada, or in a country with which Canada has a social agreement, to be eligible for Allowance", reason)
#         return reason

class afs_eligible(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether Person is eligible for allowance for survivor"

    def formula(person, period, parameters):
        """Whether Person is eligible for allowance for survivor."""
        age_requirement = person("afs_age_requirement_satisfied", period)
        widowed_requirement = person("afs_widowed_requirement_satisfied", period)
        income_requirement = person("afs_income_requirement_satisfied", period)
        residence_requirement = person("afs_residence_requirement_satisfied", period)

        return age_requirement * widowed_requirement * income_requirement * residence_requirement


class afs_eligible_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether it is known if Person is eligible for allowance for survivor"

    def formula(person, period, parameters):
        """Whether it is known if Person is eligible for allowance for survivor."""
        # A conjunction is known if any part is known false, or all parts are known
        age_false = person("afs_age_requirement_satisfied_known", period) * not_(person("afs_age_requirement_satisfied", period))
        widowed_false = person("afs_widowed_requirement_satisfied_known", period) * not_(person("afs_widowed_requirement_satisfied", period))
        income_false = person("afs_income_requirement_satisfied_known", period) * not_(person("afs_income_requirement_satisfied", period))
        residence_false = person("afs_residence_requirement_satisfied_known", period) * not_(person("afs_residence_requirement_satisfied", period))
        any_false = age_false + widowed_false + income_false + residence_false
        all_known = person("afs_age_requirement_satisfied_known", period) * person("afs_widowed_requirement_satisfied_known", period) * person("afs_income_requirement_satisfied_known", period) * person("afs_residence_requirement_satisfied_known", period)
        return any_false + all_known


class afs_age_requirement_satisfied(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the age requirement is satisfied for AFS eligibility"

    def formula(person, period, parameters):
        """Whether the age requirement is satisfied for AFS eligibility."""
        return person("afs_age_requirement_minimum_satisfied", period) * person("afs_age_requirement_cap_satisfied", period)


class afs_age_requirement_satisfied_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether it is known if the age requirement is satisfied for AFS eligibility"

    def formula(person, period, parameters):
        """Whether it is known if the age requirement is satisfied for AFS eligibility."""
        # A conjunction is known if all the elements are known or any element in known false.
        min_false = person("afs_age_requirement_minimum_satisfied_known", period) * not_(person("afs_age_requirement_minimum_satisfied", period))
        cap_false = person("afs_age_requirement_cap_satisfied_known", period) * not_(person("afs_age_requirement_cap_satisfied", period))
        any_false = min_false + cap_false
        all_known = person("afs_age_requirement_minimum_satisfied_known", period) * person("afs_age_requirement_cap_satisfied_known", period)
        return any_false + all_known


class afs_age_requirement_minimum_satisfied(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the minimum age requirement is satisfied for AFS eligibility"

    def formula(person, period, parameters):
        """Whether the minimum age requirement is satisfied for AFS eligibility."""
        minimum_age = parameters(period).benefits.old_age_security.allowance.minimum_age
        return person("age", period) >= minimum_age


class afs_age_requirement_minimum_satisfied_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether it is known if the minimum age requirement is satisfied for AFS eligibility"

    def formula(person, period, parameters):
        """Whether it is known if the minimum age requirement is satisfied for AFS eligibility."""
        return person("age_known", period)


class afs_age_requirement_cap_satisfied(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the maximum age requirement is satisfied for AFS eligibility"

    def formula(person, period, parameters):
        """Whether the maximum age requirement is satisfied for AFS eligibility."""
        cap = parameters(period).benefits.old_age_security.eligibility_age
        return person("age", period) < cap


class afs_age_requirement_cap_satisfied_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether it is known if the maximum age requirement is satisfied for AFS eligibility"

    def formula(person, period, parameters):
        """Whether it is known if the maximum age requirement is satisfied for AFS eligibility."""
        return person("age_known", period)


class afs_widowed_requirement_satisfied(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the person meets the widowed requirement for AFS eligibility"

    def formula(person, period, parameters):
        """Whether the person meets the widowed requirement for AFS eligibility."""
        married = person("marital_status", period) == marital_status_options.MARRIED
        common_law = person("marital_status", period) == marital_status_options.COMMONLAW
        widowed = person("marital_status", period) == marital_status_options.WIDOWED
        widowed_requirement = widowed * not_(married + common_law)
        return widowed_requirement


class afs_widowed_requirement_satisfied_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether it is known if the person meets the widowed requirement for AFS eligibility"

    def formula(person, period, parameters):
        """Whether it is known if the person meets the widowed requirement for AFS eligibility."""
        return person("marital_status_known", period)


class afs_income_requirement_satisfied(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the person meets the income requirement for AFS eligibility"

    def formula(person, period, parameters):
        """Whether the person meets the income requirement for AFS eligibility."""
        income_cap = parameters(period).benefits.old_age_security.allowance_for_survivor.income_cap
        income_requirement = person("income", period.this_year) < income_cap
        return income_requirement


class afs_income_requirement_satisfied_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether it is known if the person meets the income requirement for AFS eligibility"

    def formula(person, period, parameters):
        """Whether it is known if the person meets the income requirement for AFS eligibility."""
        return person("income_known", period.this_year)


class afs_residence_requirement_satisfied(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the person meets the residence requirements for AFS eligibility"

    def formula(person, period, parameters):
        """Whether the person meets the residence requirements for AFS eligibility."""
        return person("afs_residence_canadian_satisfied", period) + person("afs_residence_foreign_satisfied", period)


class afs_residence_requirement_satisfied_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the person meets the residence requirements for AFS eligibility"

    def formula(person, period, parameters):
        """Whether the person meets the residence requirements for AFS eligibility."""
        # A disjunction is known if either is known true, or both are known
        canadian_true = person("afs_residence_canadian_satisfied_known", period) * person("afs_residence_canadian_satisfied", period)
        foreign_true = person("afs_residence_foreign_satisfied_known", period) * person("afs_residence_foreign_satisfied", period)
        either_true = canadian_true + foreign_true
        both_known = person("afs_residence_canadian_satisfied_known", period) * person("afs_residence_foreign_satisfied_known", period)
        return either_true + both_known


class afs_residence_canadian_satisfied(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the person meets the Canadian residence requirements for AFS eligibility"

    def formula(person, period, parameters):
        """Whether the person meets the Canadian residence requirements for AFS eligibility."""
        return person("afs_residence_canadian_status_satisfied", period) * person("afs_residence_duration_satisfied", period)


class afs_residence_canadian_satisfied_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether it is known if the person meets the Canadian residence requirements for AFS eligibility"

    def formula(person, period, parameters):
        """Whether it is known if the person meets the Canadian residence requirements for AFS eligibility."""
        # A conjunction is known if either is known false or both are known
        canadian_false = person("afs_residence_canadian_status_satisfied_known", period) * not_(person("afs_residence_canadian_status_satisfied", period))
        duration_false = person("afs_residence_duration_satisfied_known", period) * not_(person("afs_residence_duration_satisfied", period))
        either_false = canadian_false + duration_false
        both_known = person("afs_residence_canadian_status_satisfied_known", period) * person("afs_residence_duration_satisfied_known", period)
        return either_false + both_known


class afs_residence_canadian_status_satisfied(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the person meets the residence requirements for AFS eligibility"

    def formula(person, period, parameters):
        """Whether the person meets the residence requirements for AFS eligibility."""
        citizen = person("legal_status", period) == legal_status_options.CANADIAN_CITIZEN
        indian = person("legal_status", period) == legal_status_options.STATUS_INDIAN
        perm = person("legal_status", period) == legal_status_options.PERMANENT_RESIDENT
        temp = person("legal_status", period) == legal_status_options.TEMPORARY_RESIDENT
        return citizen + indian + perm + temp


class afs_residence_canadian_status_satisfied_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether it is known if the person meets the residence requirements for AFS eligibility"

    def formula(person, period, parameters):
        """Whether it is known if the person meets the residence requirements for AFS eligibility."""
        return person("legal_status_known", period)


class afs_residence_duration_satisfied(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the person meets the residence requirements for AFS eligibility"

    def formula(person, period, parameters):
        """Whether the person meets the residence requirements for AFS eligibility."""
        minimum_years = parameters(period).benefits.old_age_security.allowance.minimum_years
        return person("years_in_canada_since_18", period) >= minimum_years


class afs_residence_duration_satisfied_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether we know if the person meets the residence requirements for AFS eligibility"

    def formula(person, period, parameters):
        """Whether we know if the person meets the residence requirements for AFS eligibility."""
        return person("years_in_canada_since_18_known", period)


class afs_residence_foreign_satisfied(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the person meets the foreign residence requirements for AFS eligibility"

    def formula(person, period, parameters):
        """Whether the person meets the foreign residence requirements for AFS eligibility."""
        return person("afs_residence_foreign_in_agreement_country_satisfied", period) * person("afs_residence_foreign_qualified_satisfied", period) * person("afs_residence_duration_satisfied", period)


class afs_residence_foreign_satisfied_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether it is known if the person meets the foreign residence requirements for AFS eligibility"

    def formula(person, period, parameters):
        """Whether it is known if the person meets the foreign residence requirements for AFS eligibility."""
        # Conjunctions are known if any are known false or all are known.
        in_agreement_false = person("afs_residence_foreign_in_agreement_country_satisfied_known", period) * not_(person("afs_residence_foreign_in_agreement_country_satisfied", period))
        qualified_false = person("afs_residence_foreign_qualified_satisfied_known", period) * not_(person("afs_residence_foreign_qualified_satisfied", period))
        duration_false = person("afs_residence_duration_satisfied_known", period) * not_(person("afs_residence_duration_satisfied", period))
        any_false = in_agreement_false + qualified_false + duration_false
        all_known = person("afs_residence_foreign_in_agreement_country_satisfied_known", period) * person("afs_residence_foreign_qualified_satisfied_known", period) * person("afs_residence_duration_satisfied_known", period)
        return any_false + all_known


class afs_residence_foreign_in_agreement_country_satisfied(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the person meets the foreign residence requirements for AFS eligibility"

    def formula(person, period, parameters):
        """Whether the person meets the foreign residence requirements for AFS eligibility."""
        return person("resides_in_agreement_country", period)


class afs_residence_foreign_in_agreement_country_satisfied_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether it is known if the person meets the foreign residence requirements for AFS eligibility"

    def formula(person, period, parameters):
        """Whether it is known if the person meets the foreign residence requirements for AFS eligibility."""
        return person("resides_in_agreement_country_known", period)


class afs_residence_foreign_qualified_satisfied(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether the person meets the foreign residence requirements for AFS eligibility"

    def formula(person, period, parameters):
        """Whether the person meets the foreign residence requirements for AFS eligibility."""
        return person("eligible_under_social_agreement", period)


class afs_residence_foreign_qualified_satisfied_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether it is known if the person meets the foreign residence requirements for AFS eligibility"

    def formula(person, period, parameters):
        """Whether it is known if the person meets the foreign residence requirements for AFS eligibility."""
        return person("eligible_under_social_agreement_known", period)


# class afs_eligible_reason(Variable):
#     value_type = str
#     entity = Person
#     definition_period = DAY
#     label = "Whether Person is eligible for allowance for survivor"

#     def formula(person, period, parameters):

#         citizen = person("legal_status",period) == legal_status_options.CANADIAN_CITIZEN
#         indian = person("legal_status",period) == legal_status_options.STATUS_INDIAN
#         perm = person("legal_status",period) == legal_status_options.PERMANENT_RESIDENT
#         temp = person("legal_status",period) == legal_status_options.TEMPORARY_RESIDENT
#         canadian_resident = citizen + indian + perm + temp

#         minimum_years = parameters(period).benefits.old_age_security.allowance.minimum_years
#         in_country_with_agreement = person("resides_in_agreement_country",period)

#         # Note that we are assuming that the age requirements are going to go along
#         # with the age requirements for the allowance itself.
#         minimum_age = parameters(period).benefits.old_age_security.allowance.minimum_age
#         # Note that we are making an assumption that the minimum age for OAS and the
#         # age cap for the allowance will always be the same value.
#         age_cap = parameters(period).benefits.old_age_security.eligibility_age
#         age = person("age",period)
#         age_requirement = (age >= minimum_age) * (age < age_cap)

#         married = person("marital_status",period) == marital_status_options.MARRIED
#         common_law = person("marital_status",period) == marital_status_options.COMMONLAW
#         widowed = person("marital_status",period) == marital_status_options.WIDOWED
#         widowed_requirement = widowed * not_(married + common_law)

#         income_cap = parameters(period).benefits.old_age_security.allowance_for_survivor.income_cap
#         income_requirement = person("income",period.this_year) < income_cap

#         years_in_canada = person("years_in_canada_since_18", period)
#         canadian_residence_requirement = canadian_resident * (years_in_canada >= minimum_years)
#         eligible_under_social_agreement = person("eligible_under_social_agreement",period)
#         alternative_residence_requirement = in_country_with_agreement * eligible_under_social_agreement * (years_in_canada >= minimum_years)

#         qualified = age_requirement * widowed_requirement * income_requirement * (canadian_residence_requirement + alternative_residence_requirement)

#         reason = where(qualified,"Based on the information provided, you are eligible for Afs!","")
#         reason = where(not_(age_requirement),"You must be between 60 and 64 to be eligible for Allowance for Survivor.",reason)
#         reason = where(not_(widowed_requirement),"You must be widowed, not common-law or married, to be eligible for Allowance for Survivor.",reason)
#         reason = where(not_(income_requirement),"Your income is too high to be eligible for Allowance for Survivor.",reason)
#         reason = where(not_(canadian_residence_requirement + alternative_residence_requirement), "You must either be a resident of Canada who has resided in Canada for 10 years, or the resident of a country with a social agreement with canada, be eligible under that agreement, and have resided in Canada for 10 years.",reason)
#         return reason

class oas_entitlement(Variable):
    value_type = float
    entity = Person
    definition_period = DAY
    label = "The amount of the person's Old Age Security entitlement"

    def formula(person, period, parameters):
        """The amount of the person's Old Age Security entitlement."""
        entitlement = 400.75 * person("oas_eligible", period)
        return entitlement


class oas_entitlement_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether we know the amount of the person's Old Age Security entitlement"

    def formula(person, period, parameters):
        """Whether we know the amount of the person's Old Age Security entitlement."""
        return person("oas_eligible_known", period)


class gis_entitlement(Variable):
    value_type = float
    entity = Person
    definition_period = DAY
    label = "The amount of the person's Guaranteed Income Supplement entitlement"

    def formula(person, period, parameters):
        """The amount of the person's Guaranteed Income Supplement entitlement."""
        entitlement = 123.45 * person("gis_eligible", period)
        return entitlement


class gis_entitlement_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether we know the amount of the person's Guaranteed Income Supplement entitlement"

    def formula(person, period, parameters):
        """Whether we know the amount of the person's Guaranteed Income Supplement entitlement."""
        return person("gis_eligible_known", period)


class allowance_entitlement(Variable):
    value_type = float
    entity = Person
    definition_period = DAY
    label = "The amount of the person's old age security allowance entitlement"

    def formula(person, period, parameters):
        """The amount of the person's old age security allowance entitlement."""
        entitlement = 23.45 * person("allowance_eligible", period)
        return entitlement


class allowance_entitlement_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether we know the amount of the person's old age security allowance entitlement"

    def formula(person, period, parameters):
        """Whether we know the amount of the person's old age security allowance entitlement."""
        return person("allowance_eligible_known", period)


class afs_entitlement(Variable):
    value_type = float
    entity = Person
    definition_period = DAY
    label = "The amount of the person's allowance for survivors entitlement"

    def formula(person, period, parameters):
        """The amount of the person's allowance for survivors entitlement."""
        entitlement = 12.34 * person("afs_eligible", period)
        return entitlement


class afs_entitlement_known(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Whether we know the amount of the person's allowance for survivors entitlement"

    def formula(person, period, parameters):
        """Whether we know the amount of the person's allowance for survivors entitlement."""
        return person("afs_eligible_known", period)
