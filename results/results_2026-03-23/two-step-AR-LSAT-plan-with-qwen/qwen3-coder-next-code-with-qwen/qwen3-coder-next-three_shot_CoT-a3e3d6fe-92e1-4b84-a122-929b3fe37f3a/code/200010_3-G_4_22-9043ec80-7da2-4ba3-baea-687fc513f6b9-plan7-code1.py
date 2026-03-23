from z3 import *

# Kitten breeds: 0-Himalayan, 1-Manx, 2-Siamese
# Puppy breeds: 0-Greyhound, 1-Newfoundland, 2-Rottweiler

# Day variables: days 1-7 (index 0-6 in lists)
kitten = [Int(f"kitten_{d}") for d in range(1, 8)]
puppy = [Int(f"puppy_{d}") for d in range(1, 8)]

solver = Solver()

# Domain constraints
for d in range(7):
    solver.add(kitten[d] >= 0, kitten[d] <= 2)
    solver.add(puppy[d] >= 0, puppy[d] <= 2)

# Fixed constraint: Greyhounds on day 1
solver.add(puppy[0] == 0)

# No consecutive breeds constraint
for d in range(6):
    solver.add(kitten[d] != kitten[d+1])
    solver.add(puppy[d] != puppy[d+1])

# Day 1 ≠ day 7 constraint
solver.add(kitten[0] != kitten[6])
solver.add(puppy[0] != puppy[6])

# Himalayan count constraint: exactly 3 days with Himalayans, none on day 1
himalayan_count = Sum([If(kitten[d] == 0, 1, 0) for d in range(7)])
solver.add(himalayan_count == 3)
solver.add(kitten[0] != 0)  # Not on day 1

# Rottweiler constraints
solver.add(puppy[6] != 2)  # Not on day 7
for d in range(7):
    solver.add(Implies(kitten[d] == 0, puppy[d] != 2))

# Extra conditional assumption: Himalayans not on day 7
solver.add(kitten[6] != 0)

# Answer choice pairs (day numbers converted to 0-indexed)
answer_pairs = [(0, 2), (1, 5), (2, 4), (3, 5), (4, 6)]

answer_index_list = []
for idx, (d1, d2) in enumerate(answer_pairs):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Same kitten breed and same puppy breed on both days
    s_chk.add(kitten[d1] == kitten[d2])
    s_chk.add(puppy[d1] == puppy[d2])
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)