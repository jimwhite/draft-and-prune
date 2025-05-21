from z3 import *

# Variables
schedule = Array('schedule', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints
w = Int('w')
solver.add(ForAll([w], And(schedule[w] >= 0, schedule[w] <= 2))) # Constraint 1
solver.add(schedule[0] != schedule[1]) # Constraint 2
solver.add(schedule[3] == 2) # Constraint 3
solver.add(Sum([If(schedule[w] == 1, 1, 0) for w in range(5)]) == 2) # Constraint 4
solver.add(schedule[2] != 0) # Constraint 5
solver.add(Sum([If(schedule[w] == 0, 1, 0) for w in range(5)]) >= 1) # Constraint 6
solver.add(schedule[4] == 2) # Constraint 7

# Answer choices
options = [
    schedule[0] == 0,  # A
    schedule[1] == 0,  # B
    Sum([If(schedule[w] == 0, 1, 0) for w in range(5)]) == 1,  # C
    Sum([If(schedule[w] == 0, 1, 0) for w in range(5)]) == 2,  # D
    schedule[1] == schedule[2]  # E
]

for i in range(len(options)):
    solver.push()
    solver.add(Not(options[i]))
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()