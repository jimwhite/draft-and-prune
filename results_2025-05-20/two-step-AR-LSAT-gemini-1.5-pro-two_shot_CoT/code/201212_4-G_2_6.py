from z3 import *

# Variables
schedule = Array('schedule', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints
solver.add(And([And(schedule[w] >= 0, schedule[w] <= 2) for w in range(5)]))  # Domain
solver.add(schedule[0] != schedule[1])  # Franco != Garcia
solver.add(schedule[3] == 2)  # Iturbe on Wednesday
solver.add(Sum([If(schedule[w] == 1, 1, 0) for w in range(5)]) == 2)  # Two on Tuesday
solver.add(schedule[2] != 0)  # Hong not on Monday
solver.add(Sum([If(schedule[w] == 0, 1, 0) for w in range(5)]) >= 1)  # At least one on Monday

# Answer choices
choices = [
    [0, 2, 1, 1, 2],  # Monday: Franco, Tuesday: Hong and Iturbe, Wednesday: Garcia and Jackson
    [0, 0, 1, 1, 2],  # Monday: Franco and Hong, Tuesday: Iturbe and Jackson, Wednesday: Garcia
    [1, 0, 2, 1, 2],  # Monday: Garcia, Tuesday: Franco and Iturbe, Wednesday: Hong and Jackson
    [1, 1, 0, 0, 2],  # Monday: Garcia and Jackson, Tuesday: Franco and Hong, Wednesday: Iturbe
    [1, 1, 1, 2, 0]  # Monday: Garcia and Jackson, Tuesday: Hong, Wednesday: Franco and Iturbe
]

# Check each choice
for i, choice in enumerate(choices):
    solver.push()
    for w in range(5):
        solver.add(schedule[w] == choice[w])
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()