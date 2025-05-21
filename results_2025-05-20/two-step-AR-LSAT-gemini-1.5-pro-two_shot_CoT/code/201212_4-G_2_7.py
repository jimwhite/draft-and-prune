from z3 import *

# Variables
schedule = Array('schedule', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints
w = Int('w')
solver.add(ForAll([w], And(schedule[w] >= 0, schedule[w] <= 2)))  # Domain
solver.add(schedule[0] != schedule[1])  # Franco != Garcia
solver.add(schedule[3] == 2)  # Iturbe on Wednesday
solver.add(Sum([If(schedule[w] == 1, 1, 0) for w in range(5)]) == 2)  # Two on Tuesday
solver.add(schedule[2] != 0)  # Hong not on Monday
solver.add(Sum([If(schedule[w] == 0, 1, 0) for w in range(5)]) >= 1)  # At least one on Monday

# Answer choices
options = [
    # A: Franco is the only witness scheduled to testify on Monday.
    [Sum([If(schedule[w] == 0, 1, 0) for w in range(5)]) == 1, schedule[0] == 0],
    # B: Franco is scheduled to testify on the same day as Iturbe.
    [schedule[0] == schedule[3]],
    # C: Garcia and Hong are both scheduled to testify on Tuesday.
    [schedule[1] == 1, schedule[2] == 1],
    # D: Garcia is the only witness scheduled to testify on Monday and Hong is one of two witnesses scheduled to testify on Wednesday.
    [Sum([If(schedule[w] == 0, 1, 0) for w in range(5)]) == 1, schedule[1] == 0,
     Sum([If(schedule[w] == 2, 1, 0) for w in range(5)]) == 2, schedule[2] == 2],
    # E: Jackson is scheduled to testify on Tuesday and two witnesses are scheduled to testify on Monday.
    [schedule[4] == 1, Sum([If(schedule[w] == 0, 1, 0) for w in range(5)]) == 2]
]

# Check each option
for i, option in enumerate(options):
    solver.push()
    solver.add(option)
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()