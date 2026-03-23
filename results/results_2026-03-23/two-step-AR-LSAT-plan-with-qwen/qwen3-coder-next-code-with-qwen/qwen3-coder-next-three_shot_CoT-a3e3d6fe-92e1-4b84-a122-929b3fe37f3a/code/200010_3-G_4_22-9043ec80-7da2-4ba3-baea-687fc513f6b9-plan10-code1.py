from z3 import *

# Kitten breeds: 0-Himalayan, 1-Manx, 2-Siamese
# Puppy breeds: 0-Greyhound, 1-Newfoundland, 2-Rottweiler
HIMALAYAN = 0
MANX = 1
SIAMESE = 2
GREYHOUND = 0
NEWFOUNDLAND = 1
ROTTWEILER = 2

# Day variables: 0-based (day 1 = index 0, ..., day 7 = index 6)
kitten = [Int(f"kitten_{i}") for i in range(7)]
puppy = [Int(f"puppy_{i}") for i in range(7)]

solver = Solver()

# Domain constraints: each breed is one of the three options
for i in range(7):
    solver.add(Or(kitten[i] == HIMALAYAN, kitten[i] == MANX, kitten[i] == SIAMESE))
    solver.add(Or(puppy[i] == GREYHOUND, puppy[i] == NEWFOUNDLAND, puppy[i] == ROTTWEILER))

# Fixed constraint: Greyhounds on day 1 (index 0)
solver.add(puppy[0] == GREYHOUND)

# No consecutive days same breed
for i in range(1, 7):
    solver.add(kitten[i] != kitten[i-1])
    solver.add(puppy[i] != puppy[i-1])

# Day 7 exclusion: same breed as day 1 not allowed on day 7
solver.add(kitten[0] != kitten[6])
solver.add(puppy[0] != puppy[6])

# Himalayan count: exactly 3 days
himalayan_count = Sum([If(kitten[i] == HIMALAYAN, 1, 0) for i in range(7)])
solver.add(himalayan_count == 3)

# Himalayans not on day 1
solver.add(kitten[0] != HIMALAYAN)

# Rottweiler not on day 7
solver.add(puppy[6] != ROTTWEILER)

# Rottweiler not on any day with Himalayans
for i in range(7):
    solver.add(Implies(kitten[i] == HIMALAYAN, puppy[i] != ROTTWEILER))

# Additional assumption: Himalayans not on day 7
solver.add(kitten[6] != HIMALAYAN)

# Answer choices: pairs of days (0-based indices)
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