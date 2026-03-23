from z3 import *

# Cookie types: 0=Oatmeal, 1=Peanut Butter, 2=Sugar
# Batches: 1=first, 2=second, 3=third

O1, O2, O3 = Ints('O1 O2 O3')
P1, P2, P3 = Ints('P1 P2 P3')
S1, S2, S3 = Ints('S1 S2 S3')

# All variables
vars_list = [O1, O2, O3, P1, P2, P3, S1, S2, S3]

solver = Solver()

# Domain constraints: each batch on day 1-5
for v in vars_list:
    solver.add(v >= 1, v <= 5)

# No duplicate days per cookie type
solver.add(O1 != O2, O1 != O3, O2 != O3)
solver.add(P1 != P2, P1 != P3, P2 != P3)
solver.add(S1 != S2, S1 != S3, S2 != S3)

# Fixed constraints
solver.add(S2 == 4)  # Second batch of sugar is Thursday (day 4)
solver.add(O2 == P1)  # Second oatmeal same day as first peanut butter

# At least one batch on Monday
solver.add(Or([v == 1 for v in vars_list]))

# Hypothetical condition: first batch of one type same day as third batch of another
hypothetical_cond = Or(
    O1 == P3,
    O1 == S3,
    P1 == O3,
    P1 == S3,
    S1 == O3,
    S1 == P3
)

# Helper function to count batches on a given day
def count_on_day(day_val):
    return Sum([If(v == day_val, 1, 0) for v in vars_list])

# Answer choices
answer_choices = [
    "At least one batch on each day",  # A: count_on_day(1)+...+count_on_day(5) == 9 and all days used
    "At least two batches on Wednesday",  # B: count_on_day(3) >= 2
    "Exactly one batch on Monday",  # C: count_on_day(1) == 1
    "Exactly two batches on Tuesday",  # D: count_on_day(2) == 2
    "Exactly one batch on Friday"   # E: count_on_day(5) == 1
]

# For each choice, check if it could be false under the hypothetical condition
answer_index_list = []

for idx in range(5):
    # Check if choice could be false
    s_chk = Solver()
    
    # Add base constraints + hypothetical condition
    s_chk.add(solver.assertions())
    s_chk.add(hypothetical_cond)
    
    # Assert the choice is false
    if idx == 0:  # A: At least one batch on each day -> false means some day has zero batches
        # Not(all days used) = at least one day unused
        s_chk.add(Or(
            count_on_day(1) == 0,
            count_on_day(2) == 0,
            count_on_day(3) == 0,
            count_on_day(4) == 0,
            count_on_day(5) == 0
        ))
    elif idx == 1:  # B: At least two batches on Wednesday -> false means <2 batches
        s_chk.add(count_on_day(3) < 2)
    elif idx == 2:  # C: Exactly one batch on Monday -> false means !=1
        s_chk.add(count_on_day(1) != 1)
    elif idx == 3:  # D: Exactly two batches on Tuesday -> false means !=2
        s_chk.add(count_on_day(2) != 2)
    elif idx == 4:  # E: Exactly one batch on Friday -> false means !=1
        s_chk.add(count_on_day(5) != 1)
    
    # If this is SAT, then the choice could be false
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)