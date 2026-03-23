from z3 import *

# Breed indices: Kitten breeds (0=Himalayan, 1=Manx, 2=Siamese)
#                Puppy breeds (0=Greyhound, 1=Newfoundland, 2=Rottweiler)

# Variables for kitten and puppy breeds on each day (0-indexed: days 1-7 -> indices 0-6)
kitten = [Int(f"k_{i}") for i in range(7)]
puppy = [Int(f"p_{i}") for i in range(7)]

solver = Solver()

# Domain constraints: each breed index must be 0, 1, or 2
for i in range(7):
    solver.add(Or(kitten[i] == 0, kitten[i] == 1, kitten[i] == 2))
    solver.add(Or(puppy[i] == 0, puppy[i] == 1, puppy[i] == 2))

# Fixed constraint: Greyhound on day 1 (index 0)
solver.add(puppy[0] == 0)

# No consecutive same breeds
for i in range(1, 7):
    solver.add(kitten[i-1] != kitten[i])
    solver.add(puppy[i-1] != puppy[i])

# Day 1 ≠ day 7
solver.add(kitten[0] != kitten[6])
solver.add(puppy[0] != puppy[6])

# Himalayan constraints:
# - Exactly 3 days with Himalayans (kitten[i] == 0)
himalayan_count = Sum([If(kitten[i] == 0, 1, 0) for i in range(7)])
solver.add(himalayan_count == 3)
# - Not on day 1 (index 0): kitten[0] != 0
solver.add(kitten[0] != 0)
# - Additional conditional assumption: NOT on day 7 (index 6): kitten[6] != 0
solver.add(kitten[6] != 0)

# Rottweiler constraints (Rottweiler = 2):
# - Not on day 7: puppy[6] != 2
solver.add(puppy[6] != 2)
# - Not on any day with Himalayans: for all i, if kitten[i] == 0 then puppy[i] != 2
for i in range(7):
    solver.add(Implies(kitten[i] == 0, puppy[i] != 2))

# Answer choices: pairs of days (1-indexed), convert to 0-indexed
answer_choices = [
    (0, 2),   # day 1 and day 3
    (1, 5),   # day 2 and day 6
    (2, 4),   # day 3 and day 5
    (3, 5),   # day 4 and day 6
    (4, 6)    # day 5 and day 7
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