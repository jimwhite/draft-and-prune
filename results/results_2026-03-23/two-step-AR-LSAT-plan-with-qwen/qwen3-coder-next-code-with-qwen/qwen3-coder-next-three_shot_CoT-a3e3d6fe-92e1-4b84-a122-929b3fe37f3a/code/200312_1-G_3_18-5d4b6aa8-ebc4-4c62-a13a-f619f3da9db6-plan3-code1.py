from z3 import *

# Cookie types: 0-oatmeal, 1-peanut butter, 2-sugar
# Days: 1=Mon, 2=Tue, 3=Wed, 4=Thu, 5=Fri

# Batch variables: b1_o, b2_o, b3_o for oatmeal; similarly for peanut butter and sugar
b1_o = Int('b1_o')
b2_o = Int('b2_o')
b3_o = Int('b3_o')

b1_p = Int('b1_p')
b2_p = Int('b2_p')
b3_p = Int('b3_p')

b1_s = Int('b1_s')
b2_s = Int('b2_s')
b3_s = Int('b3_s')

# Base solver
solver = Solver()

# Distinctness constraints per cookie type (b1 < b2 < b3 for each)
solver.add(b1_o < b2_o, b2_o < b3_o)
solver.add(b1_p < b2_p, b2_p < b3_p)
solver.add(b1_s < b2_s, b2_s < b3_s)

# Domain constraints: all batches between 1 and 5
for var in [b1_o, b2_o, b3_o, b1_p, b2_p, b3_p, b1_s, b2_s, b3_s]:
    solver.add(var >= 1, var <= 5)

# At least one batch on Monday (day 1)
solver.add(Or(b1_o == 1, b2_o == 1, b3_o == 1,
             b1_p == 1, b2_p == 1, b3_p == 1,
             b1_s == 1, b2_s == 1, b3_s == 1))

# Second oatmeal batch same day as first peanut butter batch
solver.add(b2_o == b1_p)

# Second sugar batch on Thursday (day 4)
solver.add(b2_s == 4)

# Special condition: some type X's first batch = some other type Y's third batch
# We'll use auxiliary booleans for each possible pair and day
aux = []
for i, (X1, X2, X3) in enumerate([(b1_o, b2_o, b3_o), (b1_p, b2_p, b3_p), (b1_s, b2_s, b3_s)]):
    for j, (Y1, Y2, Y3) in enumerate([(b1_o, b2_o, b3_o), (b1_p, b2_p, b3_p), (b1_s, b2_s, b3_s)]):
        if i != j:  # different cookie types
            for day in range(1, 6):
                aux.append(Bool(f"aux_{i}_{j}_{day}"))
                # X1 = day AND Y3 = day
                solver.add(Implies(aux[-1], And(X1 == day, Y3 == day)))

# At least one of the aux conditions must hold
solver.add(Or(aux))

# Function to count batches on a given day
def count_on_day(day_val):
    return Sum([If(var == day_val, 1, 0) for var in [b1_o, b2_o, b3_o,
                                                     b1_p, b2_p, b3_p,
                                                     b1_s, b2_s, b3_s]])

# Answer choices (as indices)
# A: At least one batch on each day
# B: At least two batches on Wednesday (day 3)
# C: Exactly one batch on Monday
# D: Exactly two batches on Tuesday (day 2)
# E: Exactly one batch on Friday

answer_choices = [
    "A",  # At least one batch on each day
    "B",  # At least two batches on Wednesday
    "C",  # Exactly one batch on Monday
    "D",  # Exactly two batches on Tuesday
    "E"   # Exactly one batch on Friday
]

# Check each answer choice: if its negation is satisfiable, then it could be false
answer_index_list = []

# A: Negation = some day has 0 batches
s_A = Solver()
s_A.add(solver.assertions())
negation_A = Or(*[count_on_day(d) == 0 for d in range(1, 6)])
s_A.add(negation_A)
if s_A.check() == sat:
    answer_index_list.append(0)

# B: Negation = Wednesday has at most 1 batch
s_B = Solver()
s_B.add(solver.assertions())
negation_B = count_on_day(3) <= 1
s_B.add(negation_B)
if s_B.check() == sat:
    answer_index_list.append(1)

# C: Negation = Monday has at least 2 batches (since at least 1 is always required)
s_C = Solver()
s_C.add(solver.assertions())
negation_C = count_on_day(1) >= 2
s_C.add(negation_C)
if s_C.check() == sat:
    answer_index_list.append(2)

# D: Negation = Tuesday has not exactly 2 batches (i.e., <=1 or >=3)
s_D = Solver()
s_D.add(solver.assertions())
negation_D = Or(count_on_day(2) <= 1, count_on_day(2) >= 3)
s_D.add(negation_D)
if s_D.check() == sat:
    answer_index_list.append(3)

# E: Negation = Friday has not exactly 1 batch (i.e., 0 or >=2)
s_E = Solver()
s_E.add(solver.assertions())
negation_E = Or(count_on_day(5) == 0, count_on_day(5) >= 2)
s_E.add(negation_E)
if s_E.check() == sat:
    answer_index_list.append(4)

print(answer_index_list)