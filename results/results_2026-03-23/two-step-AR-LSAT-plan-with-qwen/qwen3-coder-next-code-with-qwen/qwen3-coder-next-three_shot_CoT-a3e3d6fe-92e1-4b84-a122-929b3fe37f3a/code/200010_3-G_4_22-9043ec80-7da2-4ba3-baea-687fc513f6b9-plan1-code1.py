from z3 import *

# Day indices: 1-7 (we'll use 0-based indexing internally for days 0..6 representing days 1..7)
# Kitten breeds: Himalayan=0, Manx=1, Siamese=2
# Puppy breeds: Greyhound=3, Newfoundland=4, Rottweiler=5

kitten = [Int(f"kitten_d{i+1}") for i in range(7)]
puppy = [Int(f"puppy_d{i+1}") for i in range(7)]

solver = Solver()

# Domain constraints
for d in range(7):
    solver.add(kitten[d] >= 0, kitten[d] <= 2)
    solver.add(puppy[d] >= 3, puppy[d] <= 5)

# No breed on consecutive days
for d in range(6):
    solver.add(kitten[d] != kitten[d+1])
    solver.add(puppy[d] != puppy[d+1])

# Fixed constraints
# Greyhounds on day 1 (index 0)
solver.add(puppy[0] == 3)

# Himalayans not on day 1 (index 0)
solver.add(kitten[0] != 0)

# Any breed on day 1 not on day 7
solver.add(kitten[6] != kitten[0])
solver.add(puppy[6] != puppy[0])

# Himalayans exactly three days total, but not on day 7
solver.add(kitten[6] != 0)
solver.add(Sum([If(kitten[d] == 0, 1, 0) for d in range(7)]) == 3)

# Rottweilers not on day 7
solver.add(puppy[6] != 5)

# Rottweilers not on any day with Himalayans
for d in range(7):
    solver.add(Implies(kitten[d] == 0, puppy[d] != 5))

# Answer choices: pairs of days (1-indexed in problem, so convert to 0-indexed)
# 'day 1 and day 3' -> (0, 2), 'day 2 and day 6' -> (1, 5), etc.
answer_pairs = [(0, 2), (1, 5), (2, 4), (3, 5), (4, 6)]

answer_index_list = []
for idx, (d1, d2) in enumerate(answer_pairs):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraint that both days have same kitten and same puppy breed
    s_chk.add(kitten[d1] == kitten[d2])
    s_chk.add(puppy[d1] == puppy[d2])
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)