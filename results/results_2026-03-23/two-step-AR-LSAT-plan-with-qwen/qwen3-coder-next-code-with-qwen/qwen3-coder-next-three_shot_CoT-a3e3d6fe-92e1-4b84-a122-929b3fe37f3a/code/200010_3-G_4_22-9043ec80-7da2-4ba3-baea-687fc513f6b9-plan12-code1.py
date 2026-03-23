from z3 import *

# Kitten breeds: 0=Himalayan, 1=Manx, 2=Siamese
# Puppy breeds: 0=Greyhound, 1=Newfoundland, 2=Rottweiler

# Day variables: 0-indexed (day 1 = index 0, ..., day 7 = index 6)
kitten = [Int(f"k_{i}") for i in range(7)]
puppy = [Int(f"p_{i}") for i in range(7)]

solver = Solver()

# Domain constraints
for i in range(7):
    solver.add(kitten[i] >= 0, kitten[i] <= 2)
    solver.add(puppy[i] >= 0, puppy[i] <= 2)

# Fixed constraint: Greyhounds on day 1 (index 0)
solver.add(puppy[0] == 0)

# No consecutive same breed constraints
for i in range(6):
    solver.add(kitten[i] != kitten[i+1])
    solver.add(puppy[i] != puppy[i+1])

# Day 1 and day 7 incompatibility
solver.add(kitten[0] != kitten[6])
solver.add(puppy[0] != puppy[6])

# Himalayan count constraint: exactly 3 days, not on day 1
solver.add(kitten[0] != 0)
solver.add(Sum([If(kitten[i] == 0, 1, 0) for i in range(7)]) == 3)

# Given condition: Himalayans not on day 7
solver.add(kitten[6] != 0)

# Rottweiler constraints: not on day 7, and not on any Himalayan day
solver.add(puppy[6] != 2)
for i in range(7):
    solver.add(Implies(kitten[i] == 0, puppy[i] != 2))

# Answer choices (convert to 0-indexed day pairs)
answer_choices = [
    (0, 2),  # day 1 and day 3
    (1, 5),  # day 2 and day 6
    (2, 4),  # day 3 and day 5
    (3, 5),  # day 4 and day 6
    (4, 6)   # day 5 and day 7
]

answer_index_list = []
for idx, (day_a, day_b) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraint that both days have identical breeds
    s_chk.add(kitten[day_a] == kitten[day_b])
    s_chk.add(puppy[day_a] == puppy[day_b])
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)