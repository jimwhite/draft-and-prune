from z3 import *

# Breed indices: kitten breeds (0=Himalayan, 1=Manx, 2=Siamese)
#                puppy breeds (0=Greyhound, 1=Newfoundland, 2=Rottweiler)

# Variables: kitten[i], puppy[i] for day i (1-indexed, so use indices 0-6 for days 1-7)
kitten = [Int(f"kitten_{d}") for d in range(7)]
puppy = [Int(f"puppy_{d}") for d in range(7)]

solver = Solver()

# Domain constraints: each breed index between 0 and 2
for d in range(7):
    solver.add(kitten[d] >= 0, kitten[d] <= 2)
    solver.add(puppy[d] >= 0, puppy[d] <= 2)

# Fixed constraints
# Greyhounds on day 1 (index 0)
solver.add(puppy[0] == 0)

# Himalayans not on day 1 (index 0)
solver.add(kitten[0] != 0)

# Himalayans on exactly three days, and not on day 7 (index 6)
himalayan_days = [If(kitten[d] == 0, 1, 0) for d in range(7)]
solver.add(Sum(himalayan_days) == 3)
solver.add(kitten[6] != 0)

# Rottweilers not on day 7 (index 6)
solver.add(puppy[6] != 2)

# Rottweilers not on any day featuring Himalayans
for d in range(7):
    solver.add(Implies(kitten[d] == 0, puppy[d] != 2))

# No breed on consecutive days
for d in range(6):
    solver.add(kitten[d] != kitten[d+1])
    solver.add(puppy[d] != puppy[d+1])

# No breed on day 1 appears on day 7
solver.add(kitten[0] != kitten[6])
solver.add(puppy[0] != puppy[6])

# Answer choices: pairs of days (convert to 0-indexed)
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
    s_chk.add(kitten[d1] == kitten[d2])
    s_chk.add(puppy[d1] == puppy[d2])
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)