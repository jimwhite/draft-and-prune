from z3 import *

# Kitten breeds: 0-Himalayan, 1-Manx, 2-Siamese
# Puppy breeds: 0-Greyhound, 1-Newfoundland, 2-Rottweiler

# Variables for each day (1-7)
kitten = [Int(f"kitten_d{d}") for d in range(8)]  # index 0 unused, use 1-7
puppy = [Int(f"puppy_d{d}") for d in range(8)]    # index 0 unused, use 1-7

solver = Solver()

# Domain constraints: each breed variable in {0,1,2}
for d in range(1, 8):
    solver.add(kitten[d] >= 0, kitten[d] <= 2)
    solver.add(puppy[d] >= 0, puppy[d] <= 2)

# Fixed constraints
solver.add(puppy[1] == 0)  # Greyhounds on day 1

# No consecutive same breed constraints
for d in range(1, 7):
    solver.add(kitten[d] != kitten[d+1])
    solver.add(puppy[d] != puppy[d+1])

# Day 1 not same as day 7
solver.add(kitten[1] != kitten[7])
solver.add(puppy[1] != puppy[7])

# Himalayan constraints
solver.add(kitten[1] != 0)  # Not on day 1
solver.add(kitten[7] != 0)  # Given in conditional: not on day 7
# Exactly three days feature Himalayans
himalayan_days = [If(kitten[d] == 0, 1, 0) for d in range(1, 8)]
solver.add(Sum(himalayan_days) == 3)

# Rottweiler constraints
solver.add(puppy[7] != 2)  # Not on day 7
# Not on any day with Himalayans
for d in range(1, 8):
    solver.add(Implies(kitten[d] == 0, puppy[d] != 2))

# Answer choices: pairs of days
answer_choices = [
    (1, 3),
    (2, 6),
    (3, 5),
    (4, 6),
    (5, 7)
]

# Check each answer choice
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