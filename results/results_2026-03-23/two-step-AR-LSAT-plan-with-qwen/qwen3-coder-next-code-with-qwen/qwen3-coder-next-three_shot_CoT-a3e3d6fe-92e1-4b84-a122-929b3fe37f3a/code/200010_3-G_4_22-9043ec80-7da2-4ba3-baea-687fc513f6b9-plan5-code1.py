from z3 import *

# Kitten breeds: 0-Himalayan, 1-Manx, 2-Siamese
# Puppy breeds: 0-Greyhound, 1-Newfoundland, 2-Rottweiler

# Variables for each day (0-indexed: day1=0, ..., day7=6)
kitten = [Int(f"k_{i}") for i in range(7)]
puppy = [Int(f"p_{i}") for i in range(7)]

solver = Solver()

# Domain constraints
for i in range(7):
    solver.add(kitten[i] >= 0, kitten[i] <= 2)
    solver.add(puppy[i] >= 0, puppy[i] <= 2)

# Fixed-day constraints
solver.add(puppy[0] == 0)  # Day 1 puppy = Greyhound
solver.add(kitten[0] != 0)  # Himalayans not on day 1
solver.add(kitten[6] != 0)  # Himalayans not on day 7 (given condition)
solver.add(puppy[6] != 2)   # Day 7 puppy ≠ Rottweiler

# Himalayans on exactly three days
himalayan_count = Sum([If(kitten[i] == 0, 1, 0) for i in range(7)])
solver.add(himalayan_count == 3)

# No consecutive days with same breed
for i in range(1, 7):
    solver.add(kitten[i] != kitten[i-1])
    solver.add(puppy[i] != puppy[i-1])

# Day 1 and day 7 breeds differ
solver.add(kitten[0] != kitten[6])
solver.add(puppy[0] != puppy[6])

# Rottweiler-Himalayan exclusion: if Himalayan, then not Rottweiler
for i in range(7):
    solver.add(Implies(kitten[i] == 0, puppy[i] != 2))

# Answer choices: pairs of days (convert to 0-indexed)
answer_choices = [(0, 2), (1, 5), (2, 4), (3, 5), (4, 6)]

answer_index_list = []
for idx, (d1, d2) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraint that both days have identical kitten and puppy breeds
    s_chk.add(kitten[d1] == kitten[d2])
    s_chk.add(puppy[d1] == puppy[d2])
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)