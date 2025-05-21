from z3 import *

# Variables
kitten_breed = Array('kitten_breed', IntSort(), IntSort())
puppy_breed = Array('puppy_breed', IntSort(), IntSort())
d = Int('d')

# Solver
solver = Solver()

# Constraints 0-1
solver.add(ForAll([d], And(kitten_breed[d] >= 0, kitten_breed[d] < 3)))
solver.add(ForAll([d], And(puppy_breed[d] >= 0, puppy_breed[d] < 3)))

# Constraints 2-11
for day in range(7):
    if day < 6:
        solver.add(kitten_breed[day] != kitten_breed[day + 1])
        solver.add(puppy_breed[day] != puppy_breed[day + 1])
    if day < 7:
        if day == 0:
            solver.add(puppy_breed[day] == 0)
            solver.add(kitten_breed[day] != kitten_breed[6])
            solver.add(puppy_breed[day] != puppy_breed[6])
            solver.add(kitten_breed[day] != 0)
        elif day == 6:
            solver.add(puppy_breed[day] != 2)
            solver.add(kitten_breed[day] != 0)
        solver.add(Implies(kitten_breed[day] == 0, puppy_breed[day] != 2))

solver.add(Sum([If(kitten_breed[day] == 0, 1, 0) for day in range(7)]) == 3)


# Answer choices
choices = [
    (1, 3),
    (2, 6),
    (3, 5),
    (4, 6),
    (5, 7)
]

# Check each answer choice
for i, (day_a, day_b) in enumerate(choices):
    solver.push()
    solver.add(And(kitten_breed[day_a - 1] == kitten_breed[day_b - 1],
                   puppy_breed[day_a - 1] == puppy_breed[day_b - 1]))
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()