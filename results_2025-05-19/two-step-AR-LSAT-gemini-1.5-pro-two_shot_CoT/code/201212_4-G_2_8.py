from z3 import *

# Define variables
schedule = Array('schedule', IntSort(), IntSort())
solver = Solver()

# Witness IDs: Franco (0), Garcia (1), Hong (2), Iturbe (3), Jackson (4)
# Day IDs: Monday (0), Tuesday (1), Wednesday (2)

# Constraint 1: Domain
w = Int('w')
solver.add(ForAll([w], And(schedule[w] >= 0, schedule[w] <= 2)))

# Constraint 2: One Day Each
solver.add(Distinct([schedule[i] for i in range(5)]))

# Constraint 3: Franco and Garcia
solver.add(schedule[0] != schedule[1])

# Constraint 4: Iturbe
solver.add(schedule[3] == 2)

# Constraint 5: Tuesday
solver.add(Sum([If(schedule[w] == 1, 1, 0) for w in range(5)]) == 2)

# Constraint 6: Hong
solver.add(schedule[2] != 0)

# Constraint 7: Monday
solver.add(Sum([If(schedule[w] == 0, 1, 0) for w in range(5)]) >= 1)

# Constraint 8: Jackson
solver.add(schedule[4] == 2)

# Answer choices
options = [
    schedule[0] == 0,  # A: Franco is scheduled to testify on Monday
    schedule[1] == 0,  # B: Garcia is scheduled to testify on Monday
    Sum([If(schedule[w] == 0, 1, 0) for w in range(5)]) == 1,  # C: Exactly one witness is scheduled to testify on Monday
    Sum([If(schedule[w] == 0, 1, 0) for w in range(5)]) == 2,  # D: Exactly two witnesses are scheduled to testify on Monday
    schedule[1] == schedule[2]  # E: Garcia is scheduled to testify on the same day as Hong
]

for i in range(len(options)):
    solver.push()
    solver.add(Not(options[i]))
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()