from z3 import *

# Variables
kitten_breed = Array('kitten_breed', IntSort(), IntSort())
puppy_breed = Array('puppy_breed', IntSort(), IntSort())
d = Int('d')

# Solver
solver = Solver()

# Constraints 1 & 2 (Breed Domains)
solver.add(ForAll([d], And(kitten_breed[d] >= 0, kitten_breed[d] < 3)))
solver.add(ForAll([d], And(puppy_breed[d] >= 0, puppy_breed[d] < 3)))


# Constraints 3 & 4 (One Breed per Day - Simplified)
for i in range(7):
    solver.add(And(kitten_breed[i] >= 0, kitten_breed[i] < 3))
    solver.add(And(puppy_breed[i] >= 0, puppy_breed[i] < 3))

# Constraints 5 & 6 (No Consecutive Breeds)
for i in range(6):
    solver.add(kitten_breed[i] != kitten_breed[i+1])
    solver.add(puppy_breed[i] != puppy_breed[i+1])

# Constraints 7-14 (Specific Conditions)
solver.add(puppy_breed[0] == 0)
solver.add(kitten_breed[0] != kitten_breed[6])
solver.add(puppy_breed[0] != puppy_breed[6])
solver.add(Sum([If(kitten_breed[i] == 0, 1, 0) for i in range(7)]) == 3)
solver.add(kitten_breed[0] != 0)
solver.add(puppy_breed[6] != 2)
solver.add(ForAll([d], Implies(kitten_breed[d] == 0, puppy_breed[d] != 2)))
solver.add(kitten_breed[1] != 0)

# Check Answer Choices
answer_choices = [
    (kitten_breed[2] == 1, 'A'),
    (kitten_breed[3] == 2, 'B'),
    (puppy_breed[4] == 2, 'C'),
    (kitten_breed[5] == 0, 'D'),
    (puppy_breed[6] == 0, 'E')
]

for constraint, option in answer_choices:
    solver.push()
    solver.add(constraint)
    if solver.check() == sat:
        print(f"Option {option} is correct")
        exit()
    solver.pop()