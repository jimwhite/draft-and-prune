from z3 import *

# Variables
schedule = Array('schedule', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints
w = Int('w')
solver.add(ForAll([w], And(schedule[w] >= 0, schedule[w] <= 2)))  # Domain
solver.add(Distinct([schedule[0], schedule[1], schedule[2], schedule[3], schedule[4]]))  # Distinct Days
solver.add(schedule[0] != schedule[1])  # Franco != Garcia
solver.add(schedule[3] == 2)  # Iturbe on Wednesday
solver.add(Sum([If(schedule[w] == 1, 1, 0) for w in range(5)]) == 2)  # Two on Tuesday
solver.add(schedule[2] != 0)  # Hong not on Monday
solver.add(Sum([If(schedule[w] == 0, 1, 0) for w in range(5)]) >= 1)  # At least one on Monday

# Answer Choices
options = [
    # A
    [Sum([If(schedule[w] == 0, 1, 0) for w in range(5)]) == 1, schedule[0] == 0],
    # B
    [schedule[0] == schedule[3]],
    # C
    [schedule[1] == 1, schedule[2] == 1],
    # D
    [Sum([If(schedule[w] == 0, 1, 0) for w in range(5)]) == 1, schedule[1] == 0,
     Sum([If(schedule[w] == 2, 1, 0) for w in range(5)]) == 2, schedule[2] == 2, schedule[3] == 2],
    # E
    [schedule[4] == 1, Sum([If(schedule[w] == 0, 1, 0) for w in range(5)]) == 2]
]

for i, option in enumerate(options):
    solver.push()
    solver.add(option)
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()