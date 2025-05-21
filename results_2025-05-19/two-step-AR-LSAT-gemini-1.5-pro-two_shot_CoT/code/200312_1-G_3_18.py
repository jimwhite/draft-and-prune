from z3 import *

# Variables
schedule = Array('schedule', IntSort(), IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints
solver.add(ForAll([c, b], And(schedule[c][b] >= 0, schedule[c][b] <= 4)))  # Domain
solver.add(ForAll([c, b1, b2], Implies(b1 != b2, schedule[c][b1] != schedule[c][b2])))  # Unique Batch Days
solver.add(ForAll([c1, c2, b], Implies(And(c1 != c2, schedule[c1][b] == schedule[c2][b]), False))) # Unique Cookie Batches per Day

solver.add(Or(schedule[0][0] == 0, schedule[1][0] == 0, schedule[2][0] == 0)) # Monday Baking
solver.add(schedule[0][1] == schedule[1][0]) # Oatmeal/Peanut Butter
solver.add(schedule[2][1] == 3) # Sugar
solver.add(Or(
    schedule[0][0] == schedule[1][2], schedule[0][0] == schedule[2][2],
    schedule[1][0] == schedule[0][2], schedule[1][0] == schedule[2][2],
    schedule[2][0] == schedule[0][2], schedule[2][0] == schedule[1][2]
)) # One of First/Third Same Day


# Answer Choices
choices = [
    Or([Not(Or([Or(schedule[c][b] == d) for c in range(3) for b in range(3)])) for d in range(5)]),
    Not(Sum([If(schedule[c][b] == 2, 1, 0) for c in range(3) for b in range(3)]) >= 2),
    Not(Sum([If(schedule[c][b] == 0, 1, 0) for c in range(3) for b in range(3)]) == 1),
    Not(Sum([If(schedule[c][b] == 1, 1, 0) for c in range(3) for b in range(3)]) == 2),
    Not(Sum([If(schedule[c][b] == 4, 1, 0) for c in range(3) for b in range(3)]) == 1)
]

for i in range(len(choices)):
    solver.push()
    solver.add(choices[i])
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
