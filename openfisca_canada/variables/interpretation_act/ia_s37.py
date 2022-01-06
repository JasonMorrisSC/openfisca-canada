
from openfisca_canada.entities import Person
from openfisca_core.variables import Variable
from openfisca_core.periods import DAY, YEAR, MONTH, instant

# Construction of year
# 37 (1) The expression year means any period of twelve consecutive months, except that a reference
# (a) to a calendar year means a period of twelve consecutive months commencing on January 1;
# (b) to a financial year or fiscal year means, in relation to money provided by Parliament, 
# or the Consolidated Revenue Fund, or the accounts, taxes or finances of Canada, 
# the period beginning on April 1 in one calendar year and ending on March 31 in the 
# next calendar year; and
# (c) by number to a Dominical year means the period of twelve consecutive months commencing on January 1 of that Dominical year.

class ia_37_1_b_fiscal_year(Variable):
    value_type = str
    entity = Person
    definition_period = DAY
    label = "The period string describing the fiscal year of the given period."

    def formula(person, period, parameters):
        year = period.start.year
        month = period.start.month
        if month >= 4:
            start_year = year
        else:
            start_year = year - 1
        return str(instant(str(start_year) + "-04").period('month',12))


