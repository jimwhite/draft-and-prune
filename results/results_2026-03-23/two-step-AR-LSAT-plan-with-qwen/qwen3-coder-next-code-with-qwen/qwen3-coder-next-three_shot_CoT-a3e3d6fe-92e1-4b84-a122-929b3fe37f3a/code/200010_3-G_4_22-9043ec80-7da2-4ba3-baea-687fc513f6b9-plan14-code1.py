from z3 import *

# Day indices: 1-7 (we'll use 0-based indexing internally for arrays, but map to days 1-7)
# Kitten breeds: Himalayan=0, Manx=1, Siamese=2
# Puppy breeds: Greyhound=3, Newfoundland=4, Rottweiler=5

k = [Int(f"k_{i}") for i in range(7)]  # k[0] = day 1, ..., k[6] = day 7
p = [Int(f"p_{i}") for i in range(7)]  # p[0] = day 1, ..., p[6] = day 7

solver = Solver()

# Domain constraints
for i in range(7):
    solver.add(k[i] >= 0, k[i] <= 2)
    solver.add(p[i] >= 3, p[i] <= 5)

# Fixed constraints
solver.add(p[0] == 3)  # Greyhounds on day 1 (index 0)
solver.add(k[0] != 0)  # Himalayans not on day 1
solver.add(k[6] != 0)  # Himalayans not on day 7 (given assumption)

# Rottweilers not on day 7
solver.add(p[6] != 5)

# Himalayans featured on exactly three days
himalayan_count = Sum([If(k[i] == 0, 1, 0) for i in range(7)])
solver.add(himalayan_count == 3)

# Rottweilers not on any day with Himalayans
for i in range(7):
    solver.add(Implies(k[i] == 0, p[i] != 5))

# No breed on consecutive days
for i in range(6):
    solver.add(k[i] != k[i+1])
    solver.add(p[i] != p[i+1])

# Day 1 and day 7 breeds must be different
solver.add(k[0] != k[6])
solver.add(p[0] != p[6])

# Answer choices: pairs of days (1-indexed), convert to 0-indexed
answer_choices = [(0, 2), (1, 5), (2, 4), (3, 5), (4, 6)]  # (day1-1, day2-1)

answer_index_list = []
for idx, (d1, d2) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraint that both days have same kitten and puppy breeds
    s_chk.add(k[d1] == k[d2])
    s_chk.add(p[d1] == p[d2])
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)