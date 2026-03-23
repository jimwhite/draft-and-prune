from z3 import *

# Day indices: 1-7 (we'll use 0-based indexing internally for days, so day d in problem is index d-1)
# Kitten breeds: 0-Himalayan, 1-Manx, 2-Siamese
# Puppy breeds: 0-Greyhound, 1-Newfoundland, 2-Rottweiler

kitten = [Int(f"kitten_{d}") for d in range(7)]  # indices 0-6 represent days 1-7
puppy = [Int(f"puppy_{d}") for d in range(7)]

solver = Solver()

# Domain constraints
for d in range(7):
    solver.add(kitten[d] >= 0, kitten[d] <= 2)
    solver.add(puppy[d] >= 0, puppy[d] <= 2)

# Initial constraints
# Greyhound on day 1 (index 0)
solver.add(puppy[0] == 0)

# Himalayans not on day 1 (index 0)
solver.add(kitten[0] != 0)

# Himalayans on exactly three days total
solver.add(Sum([If(kitten[d] == 0, 1, 0) for d in range(7)]) == 3)

# Himalayans not on day 7 (index 6) - given in conditional premise
solver.add(kitten[6] != 0)

# Rottweilers not on day 7 (index 6)
solver.add(puppy[6] != 2)

# Rottweilers not on any day featuring Himalayans
for d in range(7):
    solver.add(Implies(kitten[d] == 0, puppy[d] != 2))

# No consecutive duplicate breeds
for d in range(6):
    solver.add(kitten[d] != kitten[d+1])
    solver.add(puppy[d] != puppy[d+1])

# Any breed on day 1 is not on day 7
solver.add(kitten[0] != kitten[6])
solver.add(puppy[0] != puppy[6])

# Answer choice pairs (convert to 0-based day indices)
answer_pairs = [
    (0, 2),  # day 1 and day 3 -> indices 0 and 2
    (1, 5),  # day 2 and day 6 -> indices 1 and 5
    (2, 4),  # day 3 and day 5 -> indices 2 and 4
    (3, 5),  # day 4 and day 6 -> indices 3 and 5
    (4, 6)   # day 5 and day 7 -> indices 4 and 6
]

answer_index_list = []

for idx, (d1, d2) in enumerate(answer_pairs):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraint that both days have identical kitten and puppy
    s_chk.add(kitten[d1] == kitten[d2])
    s_chk.add(puppy[d1] == puppy[d2])
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)