from z3 import *

# Day variables: 1-7 (we'll use indices 0-6 for days 1-7)
# Kitten breeds: 0=Himalayan, 1=Manx, 2=Siamese
# Puppy breeds: 0=Greyhound, 1=Newfoundland, 2=Rottweiler

k = [Int(f"k_{d}") for d in range(1, 8)]  # k[0] = day1, ..., k[6] = day7
p = [Int(f"p_{d}") for d in range(1, 8)]  # p[0] = day1, ..., p[7] = day7

solver = Solver()

# Domain constraints: kitten breeds 0-2, puppy breeds 0-2
for d in range(7):
    solver.add(k[d] >= 0, k[d] <= 2)
    solver.add(p[d] >= 0, p[d] <= 2)

# Fixed constraints
# Greyhounds on day 1 -> p[0] == 0
solver.add(p[0] == 0)

# Himalayans not on day 1 -> k[0] != 0
solver.add(k[0] != 0)

# No breed on consecutive days (for both kitten and puppy)
for d in range(6):
    solver.add(k[d] != k[d+1])
    solver.add(p[d] != p[d+1])

# Any breed on day 1 not on day 7
solver.add(Implies(k[0] == 0, k[6] != 0))
solver.add(Implies(k[0] == 1, k[6] != 1))
solver.add(Implies(k[0] == 2, k[6] != 2))
solver.add(Implies(p[0] == 0, p[6] != 0))
solver.add(Implies(p[0] == 1, p[6] != 1))
solver.add(Implies(p[0] == 2, p[6] != 2))

# Rottweilers not on day 7 -> p[6] != 2
solver.add(p[6] != 2)

# Rottweilers not on any day that features Himalayans
for d in range(7):
    solver.add(Implies(k[d] == 0, p[d] != 2))

# Himalayans on exactly three days (base constraint)
himalayan_count = Sum([If(k[d] == 0, 1, 0) for d in range(7)])
solver.add(himalayan_count == 3)

# Conditional assumption: Himalayans NOT on day 7 -> k[6] != 0
solver.add(k[6] != 0)

# Answer choices: pairs of days (1-indexed in problem, but we use 0-indexed internally)
# day 1 and day 3 -> (0,2), day 2 and day 6 -> (1,5), etc.
day_pairs = [(0, 2), (1, 5), (2, 4), (3, 5), (4, 6)]

answer_index_list = []
for idx, (d1, d2) in enumerate(day_pairs):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraint that day d1 and day d2 have identical breeds
    s_chk.add(k[d1] == k[d2])
    s_chk.add(p[d1] == p[d2])
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)