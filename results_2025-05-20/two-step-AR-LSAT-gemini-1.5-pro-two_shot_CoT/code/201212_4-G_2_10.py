from z3 import *

# Variables
schedule = Array('schedule', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints
witnesses = [0, 1, 2, 3, 4]
days = [0, 1, 2]

# Constraint 1 (Domain)
for w in witnesses:
    solver.add(schedule[w] >= 0)
    solver.add(schedule[w] <= 2)

# Constraint 2 (Franco != Garcia)
solver.add(schedule[0] != schedule[1])

# Constraint 3 (Iturbe on Wednesday)
solver.add(schedule[3] == 2)

# Constraint 4 (Two on Tuesday)
solver.add(Sum([If(schedule[w] == 1, 1, 0) for w in witnesses]) == 2)

# Constraint 5 (Hong not on Monday)
solver.add(schedule[2] != 0)

# Constraint 6 (At least one on Monday)
solver.add(Sum([If(schedule[w] == 0, 1, 0) for w in witnesses]) >= 1)

# Constraint 7 (Franco == Hong)
solver.add(schedule[0] == schedule[2])

# Answer Choices
choices = [
    schedule[0] != 2,  # A
    schedule[1] != 0,  # B
    schedule[1] != 2,  # C
    schedule[2] != 1,  # D
    Sum([If(schedule[w] == 2, 1, 0) for w in witnesses]) != 1  # E
]

for i in range(len(choices)):
    solver.push()
    solver.add(choices[i])
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
