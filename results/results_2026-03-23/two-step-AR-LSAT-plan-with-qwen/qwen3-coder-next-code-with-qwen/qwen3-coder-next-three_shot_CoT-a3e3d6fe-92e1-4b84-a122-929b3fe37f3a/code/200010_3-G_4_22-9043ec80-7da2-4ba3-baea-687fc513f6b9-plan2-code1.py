from z3 import *

# Day indices: 1 to 7 (we'll use 0-indexed internally, so day d -> index d-1)
# Kitten breeds: 0=Himalayan, 1=Manx, 2=Siamese
# Puppy breeds: 0=Greyhound, 1=Newfoundland, 2=Rottweiler

kitten = [Int(f"kitten_{d}") for d in range(1, 8)]
puppy = [Int(f"puppy_{d}") for d in range(1, 8)]

solver = Solver()

# Domain constraints
for d in range(7):
    solver.add(kitten[d] >= 0, kitten[d] <= 2)
    solver.add(puppy[d] >= 0, puppy[d] <= 2)

# Fixed constraints
# Greyhounds on day 1: puppy[0] == 0 (day 1 is index 0)
solver.add(puppy[0] == 0)

# Himalayans on exactly three days, but not day 1: kitten[0] != 0
solver.add(kitten[0] != 0)
# Exactly three Himalayans
himalayan_count = Sum([If(kitten[d] == 0, 1, 0) for d in range(7)])
solver.add(himalayan_count == 3)

# Rottweilers not on day 7: puppy[6] != 2
solver.add(puppy[6] != 2)

# Rottweilers not on any day with Himalayans
for d in range(7):
    solver.add(Implies(kitten[d] == 0, puppy[d] != 2))

# No breed on consecutive days
for d in range(6):
    solver.add(kitten[d] != kitten[d+1])
    solver.add(puppy[d] != puppy[d+1])

# Any breed on day 1 not featured on day 7
solver.add(kitten[0] != kitten[6])
solver.add(puppy[0] != puppy[6])

# Additional assumption: Himalayans not on day 7 (kitten[6] != 0)
solver.add(kitten[6] != 0)

# Answer choices: pairs of days (1-indexed), convert to 0-indexed
answer_choices = [(0, 2), (1, 5), (2, 4), (3, 5), (4, 6)]  # (1,3)->(0,2), etc.

answer_index_list = []
for idx, (d1, d2) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraint that the two days have identical breeds
    s_chk.add(kitten[d1] == kitten[d2])
    s_chk.add(puppy[d1] == puppy[d2])
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)