from z3 import *

# Variables
schedule = Array('schedule', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints
for w in range(5):  # Domain - Corrected ForAll usage
    solver.add(schedule[w] >= 0, schedule[w] <= 2)
solver.add(Distinct([schedule[0], schedule[1], schedule[2], schedule[3], schedule[4]]))  # Distinct Days
solver.add(schedule[0] != schedule[1])  # Franco != Garcia
solver.add(schedule[3] == 2)  # Iturbe on Wednesday
solver.add(Sum([If(schedule[w] == 1, 1, 0) for w in range(5)]) == 2)  # Two on Tuesday
solver.add(schedule[2] != 0)  # Hong not on Monday
solver.add(Sum([If(schedule[w] == 0, 1, 0) for w in range(5)]) >= 1)  # At least one on Monday
solver.add(schedule[0] == schedule[2])  # Franco and Hong same day

# Answer choices
answers = [
    schedule[0] != 2,  # A
    schedule[1] != 0,  # B
    schedule[1] != 2,  # C
    schedule[2] != 1,  # D
    Sum([If(schedule[w] == 2, 1, 0) for w in range(5)]) != 1  # E
]

for i in range(len(answers)):
    solver.push()
    solver.add(answers[i])
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
