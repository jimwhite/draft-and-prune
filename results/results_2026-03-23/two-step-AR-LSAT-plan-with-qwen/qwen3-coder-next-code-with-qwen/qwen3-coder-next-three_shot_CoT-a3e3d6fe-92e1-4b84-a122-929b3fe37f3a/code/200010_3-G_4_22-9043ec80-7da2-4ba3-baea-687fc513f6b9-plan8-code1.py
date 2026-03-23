from z3 import *

# Day indices: 1-7 (we'll use 0-based indexing internally, so day i corresponds to index i-1)
# Kitten breeds: Himalayan=0, Manx=1, Siamese=2
# Puppy breeds: Greyhound=3, Newfoundland=4, Rottweiler=5

k = [Int(f"k_{i}") for i in range(1, 8)]  # k[0] = day 1, ..., k[6] = day 7
p = [Int(f"p_{i}") for i in range(1, 8)]  # p[0] = day 1, ..., p[6] = day 7

solver = Solver()

# Domain constraints
for i in range(7):
    solver.add(k[i] >= 0, k[i] <= 2)
    solver.add(p[i] >= 3, p[i] <= 5)

# Fixed constraint: Greyhounds on day 1
solver.add(p[0] == 3)

# No consecutive days same breed
for i in range(6):
    solver.add(k[i] != k[i+1])
    solver.add(p[i] != p[i+1])

# Day 1 not featured on day 7
solver.add(k[0] != k[6])
solver.add(p[0] != p[6])

# Himalayans on exactly 3 days, not on day 1
solver.add(k[0] != 0)
solver.add(Sum([If(k[i] == 0, 1, 0) for i in range(7)]) == 3)

# Rottweilers not on day 7 and not on any day with Himalayans
solver.add(p[6] != 5)
for i in range(7):
    solver.add(Implies(k[i] == 0, p[i] != 5))

# Conditional assumption: Himalayans not on day 7
solver.add(k[6] != 0)

# Answer choices: pairs of days (1-indexed), convert to 0-indexed
answer_choices = [
    (0, 2),  # day 1 and day 3
    (1, 5),  # day 2 and day 6
    (2, 4),  # day 3 and day 5
    (3, 5),  # day 4 and day 6
    (4, 6)   # day 5 and day 7
]

answer_index_list = []
for idx, (d1, d2) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraint that both days have identical breeds
    s_chk.add(k[d1] == k[d2])
    s_chk.add(p[d1] == p[d2])
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)