from z3 import *

# Variables
schedule = Array('schedule', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints
w = Int('w')
solver.add(ForAll([w], And(schedule[w] >= 0, schedule[w] <= 2))) # Domain
solver.add(schedule[0] != schedule[1]) # Franco != Garcia
solver.add(schedule[3] == 2) # Iturbe on Wednesday
solver.add(Sum([If(schedule[w] == 1, 1, 0) for w in range(5)]) == 2) # Two on Tuesday
solver.add(schedule[2] != 0) # Hong not on Monday
solver.add(Sum([If(schedule[w] == 0, 1, 0) for w in range(5)]) >= 1) # At least one on Monday
solver.add(schedule[4] == 0) # Jackson only on Monday
solver.add(Sum([If(schedule[w] == 0, 1, 0) for w in range(5)]) == 1) # Jackson only on Monday


# Answer choices
options = [
    schedule[0] == 2,  # A
    schedule[2] == 1,  # B
    schedule[1] == 1,  # C
    schedule[0] == schedule[2],  # D
    schedule[1] == schedule[2]   # E
]

for i in range(len(options)):
    solver.push()
    solver.add(Not(options[i]))
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()