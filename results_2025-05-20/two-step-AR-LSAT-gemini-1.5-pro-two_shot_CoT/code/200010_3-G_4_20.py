from z3 import *

# Variables
kitten_breed = Array('kitten_breed', IntSort(), IntSort())
puppy_breed = Array('puppy_breed', IntSort(), IntSort())

solver = Solver()

# Constraints 1 & 2 (Breed Domains)
for day in range(7):
    solver.add(And(kitten_breed[day] >= 0, kitten_breed[day] < 3))
    solver.add(And(puppy_breed[day] >= 0, puppy_breed[day] < 3))

# Constraints 3 & 4 (No Consecutive Breeds)
for day in range(6):
    solver.add(kitten_breed[day] != kitten_breed[day + 1])
    solver.add(puppy_breed[day] != puppy_breed[day + 1])

# Constraint 5 (Greyhounds on Day 1)
solver.add(puppy_breed[0] == 0)

# Constraints 6 & 7 (No Day 1 Breed on Day 7)
solver.add(kitten_breed[0] != kitten_breed[6])
solver.add(puppy_breed[0] != puppy_breed[6])

# Constraint 8 (Himalayans on 3 Days)
solver.add(Sum([If(kitten_breed[day] == 0, 1, 0) for day in range(7)]) == 3)

# Constraint 9 (No Himalayans on Day 1)
solver.add(kitten_breed[0] != 0)

# Constraint 10 (No Rottweilers on Day 7)
solver.add(puppy_breed[6] != 2)

# Constraint 11 (No Rottweilers with Himalayans)
for day in range(7):
    solver.add(Implies(kitten_breed[day] == 0, puppy_breed[day] != 2))

# Additional constraint from the question (No Himalayans on Day 2)
solver.add(kitten_breed[1] != 0)

# Check answer choices
answer_choices = [
    (kitten_breed[2] == 1),  # A: Manx on day 3
    (kitten_breed[3] == 2),  # B: Siamese on day 4
    (puppy_breed[4] == 2),  # C: Rottweilers on day 5
    (kitten_breed[5] == 0),  # D: Himalayans on day 6
    (puppy_breed[6] == 0)   # E: Greyhounds on day 7
]

for i, choice in enumerate(answer_choices):
    solver.push()
    solver.add(choice)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()