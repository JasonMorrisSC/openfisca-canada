from openfisca_core.model_api import not_
from openfisca_core.periods import DAY, YEAR, MONTH, instant
from openfisca_core.variables import Variable


from openfisca_canada.entities import Person
# TODO: Encode section 7
# 
# Amount of Pension
# Basic amount of full pension

# 7 (1) The amount of the full monthly pension that may be paid to any person for a month in the 
# payment quarter commencing on January 1, 1985 is two hundred and seventy-three dollars and eighty cents.

class oas_7_1_amount_of_full_monthly_pension(Variable):
    value_type = float
    entity = Person
    definition_period = MONTH
    label = "The amount of the full monthly pension that may be paid to a person."

    def formula(person, period, parameters):
        if period.size == 1 and period.year == 1985 and period.month in [1,2,3]:
            return 273.80
        
class oas_7_1_amount_of_full_monthly_pension_known(Variable):
    value_type = float
    entity = Person
    definition_period = MONTH
    label = "The amount of the full monthly pension that may be paid to a person."

    def formula(person, period, paramaters):
        return True


# Quarterly adjustment of basic amount of full pension

# (2) Where a full monthly pension has been authorized to be paid to a person, the amount of the pension 
# shall be adjusted quarterly, in such manner as may be prescribed by regulation, so that the amount that 
# may be paid to that person for a month in any payment quarter commencing after March 31, 1985 is the 
# amount obtained by multiplying

# (a) the amount of the pension that might have been paid to that person for a month in the three month 
# period immediately before that payment quarter

# by

# (b) the ratio that the Consumer Price Index for the first adjustment quarter that relates to that payment 
# quarter bears to the Consumer Price Index for the second adjustment quarter that relates to that payment quarter.

# No decrease in amount of full pension

# (3) Notwithstanding subsection (2), the amount of a full monthly pension that may be paid to a pensioner for 
# any month in a payment quarter shall be not less than the amount of the full monthly pension that was or may 
# be paid to a pensioner for any month in the three month period immediately before that payment quarter.

# Effect of reduction in Consumer Price Index

# (4) Where, in relation to any payment quarter, the Consumer Price Index for the first adjustment quarter is 
# lower than the Consumer Price Index for the second adjustment quarter,

# (a) no pension adjustment shall be made pursuant to subsection (2) in respect of that payment quarter; and

# (b) no pension adjustment shall be made pursuant to that subsection in respect of any subsequent payment 
# quarter until, in relation to a subsequent payment quarter, the Consumer Price Index for the first adjustment 
# quarter that relates to that subsequent payment quarter is higher than the Consumer Price Index for the second 
# adjustment quarter that relates to the payment quarter referred to in paragraph (a), in which case the second 
# adjustment quarter that relates to the payment quarter referred to in that paragraph shall be deemed to be the 
# second adjustment quarter that relates to that subsequent payment quarter.

# Full monthly pension — persons aged 75 years or older

# (5) Beginning in the payment quarter commencing on July 1, 2022, for the period that begins in the month after 
# the month in which a person attains 75 years of age, the amount of the full monthly pension, as it is calculated 
# in accordance with subsections (1) to (4), is increased by 10%.