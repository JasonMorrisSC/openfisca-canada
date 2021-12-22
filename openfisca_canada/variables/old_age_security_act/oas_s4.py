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
# Regulations respecting legal residence

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

# TODO: Left off working here.

# (2) The Governor in Council may make regulations respecting the meaning of legal 
# residence for the purposes of subsection (1).

# This is an empowering provision. We don't need to encode it, because we are not going to use
# this encoding in order to figure out whether or not the governor in council acted improperly.
# We do need to review those regulations and include anything relevant in our encoding.