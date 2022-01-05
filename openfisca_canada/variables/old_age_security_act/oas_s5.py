# Limitations
# 5 (1) No pension may be paid to any person unless that person is qualified under subsection 3(1) or (2), 
# an application therefor has been made by or on behalf of that person and the application has been approved, and, 
# except as provided in this Act, no pension may be paid to any person in respect of any period prior to the day 
# on which that person’s application is approved.

# This encoding is focused on whether the person is eligible, and if so, for what amount. It is not attempting
# to determine the required sequence of events or process in advance of payment of those benefits.
# We do model the date on which the person's application is approved, and could conceivably modify the code
# calculating the amounts on the basis of the additional question of whether it relates to a period prior
# to the day on which the applicaiton is approved. It's not clear if that would be valuable.

# TODO: Determine if we have any need to encode 5(1).

# Application deemed to have been made and approved
# (2) Where an allowance ceases to be payable to a person by reason of that person having reached sixty-five years 
# of age, the Minister may deem an application under subsection (1) to have been made by that person and approved, 
# on the day on which the person reached that age.

# This deals with the procedural element of terminating an allowance. It does not impact eligibility or the amount.
# Eligibility ceases at 65 regardless.

# Incarcerated persons
# (3) No pension may be paid in respect of a period of incarceration — exclusive of the first month of that period — 
# to a person who is subject to a sentence of imprisonment
# (a) that is to be served in a penitentiary by virtue of any Act of Parliament; or
# (b) that exceeds 90 days and is to be served in a prison, as defined in subsection 2(1) of the Prisons and 
# Reformatories Act, if the government of the province in which the prison is located has entered into an agreement 
# under section 41 of the Department of Employment and Social Development Act.

# The "payability" of an entitlment is again not something that we're trying to model. We also aren't modeling
# payments as a series of events over time. We also aren't collecting inforamtion on incarceration. Not sure that
# this is useful in our current context.
# TODO: Confirm we don't need to model 5(3).

# The remainder of section 5 is procedural and enabling, and doesn't go to eligibility or entitlement.


# Waiver of application
# (4) The Minister may, on the day on which a person attains 65 years of age, waive the requirement referred to in 
# subsection (1) for an application if the Minister is satisfied, based on information that is available to him or 
# her under this Act, that the person is qualified under subsection 3(1) or (2) for the payment of a pension.


# Notice of intent
# (5) If the Minister intends to waive the requirement for an application in respect of a person, the Minister shall 
# notify the person in writing of that intention and provide them with the information on which the Minister intends 
# to rely to approve the payment of a pension.

# Inaccuracies
# (6) The person shall, before the day on which they attain 65 years of age, file with the Minister a statement in 
# which the person corrects any inaccuracies in the information provided by the Minister under subsection (5).
# Declining waiver
# (7) The person may, before the day on which they attain 65 years of age, decline a waiver of the requirement for 
# an application by notifying the Minister in writing of their decision to do so.
# Cancellation of waiver
# (8) Even if the requirement for an application is intended to be waived in respect of a person under subsection (4), 
# the Minister may, before the day on which the person attains 65 years of age, require that the person make an 
# application for payment of a pension and, in that case, the Minister shall notify the person in writing of that 
# requirement.