from z3 import *

# Day indices: 0-6 for days 1-7
k = [Int(f"k_{i}") for i in range(7)]  # kitten breeds: 0=Himalayan, 1=Manx, 2=Siamese
p = [Int(f"p_{i}") for i in range(7)]  # puppy breeds: 0=Greyhound, 1=Newfoundland, 2=Rottweiler

solver = Solver()

# Fixed constraints
# Greyhound on day 1 (index 0)
solver.add(p[0] == 0)
# Himalayans not on day 1 (index 0) and not on day 7 (index 6)
solver.add(k[0] != 0)
solver.add(k[6] != 0)

# Himalayans on exactly 3 days
himalayan_count = Sum([If(k[i] == 0, 1, 0) for i in range(7)])
solver.add(himalayan_count == 3)

# Rottweilers not on day 7 (index 6)
solver.add(p[6] != 2)

# Rottweilers not on any day that features Himalayans
for i in range(7):
    solver.add(Implies(k[i] == 0, p[i] != 2))

# No breed on consecutive days
for i in range(6):
    solver.add(k[i] != k[i+1])
    solver.add(p[i] != p[i+1])

# Day 1 and day 7 must have different breeds
solver.add(k[0] != k[6])
solver.add(p[0] != p[6])

# Domain constraints for kitten breeds (0, 1, or 2)
for i in range(7):
    solver.add(Or(k[i] == 0, k[i] == 1, k[i] == 2))

# Domain constraints for puppy breeds (0, 1, or 2)
for i in range(7):
    solver.add(Or(p[i] == 0, p[i] == 1, p[i] == 2))

# Answer choice pairs (day indices): 
# 'day 1 and day 3' -> (0,2), 'day 2 and day 6' -> (1,5), 
# 'day 3 and day 5' -> (2,4), 'day 4 and day 6' -> (3,5), 
# 'day 5 and day 7' -> (4,6)
answer_pairs = [(0, 2), (1, 5), (2, 4), (3, 5), (4, 6)]

answer_index_list = []
for idx, (d1, d2) in enumerate(answer_pairs):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraint that both days have same kitten and same puppy
    s_chk.add(k[d1] == k[d2])
    s_chk.add(p[d1] == p[d2])
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)