from z3 import *

# Day indices: 0 to 6 represent days 1 to 7
kitten = [Int(f"kitten_{i}") for i in range(7)]
puppy = [Int(f"puppy_{i}") for i in range(7)]

# Breed codes: kitten = {0: Himalayan, 1: Manx, 2: Siamese}
#              puppy = {0: Greyhound, 1: Newfoundland, 2: Rottweiler}

solver = Solver()

# Domain constraints
for i in range(7):
    solver.add(kitten[i] >= 0, kitten[i] <= 2)
    solver.add(puppy[i] >= 0, puppy[i] <= 2)

# Fixed constraint: Greyhound on day 1 (index 0)
solver.add(puppy[0] == 0)

# No consecutive days same breed
for i in range(6):
    solver.add(kitten[i] != kitten[i+1])
    solver.add(puppy[i] != puppy[i+1])

# Day 7 exception: breed on day 1 not repeated on day 7
solver.add(kitten[0] != kitten[6])
solver.add(puppy[0] != puppy[6])

# Himalayan constraint: exactly 3 days, not on day 1
himalayan_count = Sum([If(kitten[i] == 0, 1, 0) for i in range(7)])
solver.add(himalayan_count == 3)
solver.add(kitten[0] != 0)

# Rottweiler constraint: not on day 7, and not on any Himalayan day
solver.add(puppy[6] != 2)
for i in range(7):
    solver.add(Implies(kitten[i] == 0, puppy[i] != 2))

# Problem-specific conditional: Himalayans not on day 7
solver.add(kitten[6] != 0)

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
    
    # Add constraint that both days have same kitten and same puppy
    s_chk.add(kitten[d1] == kitten[d2])
    s_chk.add(puppy[d1] == puppy[d2])
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)