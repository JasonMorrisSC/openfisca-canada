from  openfisca_core.variables import Variable
from openfisca_core.periods import instant, MONTH
from openfisca_core.errors import PeriodMismatchError
from openfisca_canada.entities import Person

# first adjustment quarter, in relation to a payment quarter, means,
# (a) if the payment quarter commences on the first day of April in a payment 
# period, the period of three months commencing on the first day of November 
# immediately before that first day of April,
# (b) if the payment quarter commences on the first day of July in a payment 
# period, the period of three months commencing on the first day of February 
# immediately before that first day of July,
# (c) if the payment quarter commences on the first day of October in a payment 
# period, the period of three months commencing on the first day of May 
# immediately before that first day of October, and
# (d) if the payment quarter commences on the first day of January in a payment 
# period, the period of three months commencing on the first day of August 
# immediately before that first day of January; (premier trimestre de rajustement)

class oas_s2_first_adjustment_quarter(Variable):
  value_type = str
  entity = Person
  definition_period = MONTH
  label = "The first adjustment quarter as defined in section 2 of the OAS Act."

  def formula(person, period, parameters):
    if period.size_in_months != 3 or period.start.month not in [1,4,7,10]:
        raise PeriodMismatchError("oas_s2_first_adjustment_quarter",period,MONTH,"oas_s2_first_adjustment_quarter is defined only for payment quarters.")
    if period.start.month == 4:
        return instant(str(period.start.year-1)+"-11").period('month',3)
    elif period.start.month == 7:
        return instant(str(period.start.year)+"-02").period('month',3)
    elif period.start.month == 10:
        return instant(str(period.start.year)+"-05").period('month',3)
    elif period.start.month == 1:
        return instant(str(period.start.year-1)+"-08").period('month',3)


# payment period, in relation to a month, means
# (a) the fiscal year that includes the month, where the month 
# is before April, 1998,
# (b) the period that begins on April 1, 1998 and ends on June 
# 30, 1999, where that period includes the month, and
# (c) the period after June 30, 1999 that begins on July 1 of 
# one year and ends on June 30 of the next year, where that period 
# includes the month; (période de paiement)

class oas_s2_payment_period(Variable):
  value_type = str
  entity = Person
  definition_period = MONTH
  label = "The payment period for the person, as defined in section 2 of the OAS Act."

  def formula(person, period, parameters):
    # Need to report an error if they are trying to check for a period of duration more than 1 month.
    if period.size_in_months != 1:
      raise PeriodMismatchError("oas_s2_payment_period",period,MONTH,"oas_s2_payment_period is defined only for periods of exactly 1 month.")
    
    fiscal_years = person('ia_37_1_b_fiscal_year',period.start)

    period_start = period.start.date
    period_stop = period.stop.date
    apr_1998 = instant('1998-04').date
    apr_98_to_jun_99 = instant('1998-04').period('month',15)
    jul_1999 = instant('1999-07').date
    period_month = period.start.month
    after_july = period_month >= 7
    period_year = period.start.year
    if after_july:
      payment_start_year = period_year
    else:
      payment_start_year = period_year - 1

    payment_year = instant(str(payment_start_year) + "-07").period('month',12)

    if period_stop < apr_1998:
      payment_period = fiscal_years[0]
    elif period_stop < jul_1999 and period_start >= apr_1998:
      payment_period = str(apr_98_to_jun_99)
    elif period_start >= jul_1999:
      payment_period = str(payment_year)
    
    return payment_period

# payment quarter means a period of three months commencing 
# on the first day of April, July, October or January in a 
# payment period; (trimestre de paiement)

# TODO: Figure out if I need to encode payment quarter at all.
# I think so, yeah.

# I'm not sure how to interpret "in a payment period", here.
# If it was excluded, all calendar year quarters would be payment quarters.
# With it included, they are only payment quarters IF they are
# a period of three months "in" a payment period. That would mean
# that prior to july of 1999, there are fewer payment quarters per year.
# The other alternative is that 'in' should be taken to mean "overlapping with"
# in which case the april 98 to july 99 "payment period" has 5 payment quarters,
# one of which is shared with april 97-98.

# Perhaps the easiest way to do it would be to define it by month,
# as payment period is defined by month, and then calculate the payment quarters
# in the payment period for the given month?


# second adjustment quarter, in relation to a payment quarter, means,
# (a) if the payment quarter commences on the first day of April in a 
# payment period, the period of three months commencing on the first day 
# of August immediately before that first day of April,
# (b) if the payment quarter commences on the first day of July in a 
# payment period, the period of three months commencing on the first day 
# of November immediately before that first day of July,
# (c) if the payment quarter commences on the first day of October in a 
# payment period, the period of three months commencing on the first day 
# of February immediately before that first day of October, and
# (d) if the payment quarter commences on the first day of January in a 
# payment period, the period of three months commencing on the first day 
# of May immediately before that first day of January; (second trimestre de rajustement)

class oas_s2_second_adjustment_quarter(Variable):
  value_type = str
  entity = Person
  definition_period = MONTH
  label = "The second adjustment quarter as defined under section 2 of the OAS Act."

  def formula(person, period, parameters):
    if period.size_in_months != 3 or period.start.month not in [1,4,7,10]:
        raise PeriodMismatchError("oas_s2_second_adjustment_quarter",period,MONTH,"oas_s2_second_adjustment_quarter is defined only for payment quarters.")
    if period.start.month == 4:
        return instant(str(period.start.year-1)+"-08").period('month',3)
    elif period.start.month == 7:
        return instant(str(period.start.year-1)+"-11").period('month',3)
    elif period.start.month == 10:
        return instant(str(period.start.year)+"-02").period('month',3)
    elif period.start.month == 1:
        return instant(str(period.start.year-1)+"-05").period('month',3)
