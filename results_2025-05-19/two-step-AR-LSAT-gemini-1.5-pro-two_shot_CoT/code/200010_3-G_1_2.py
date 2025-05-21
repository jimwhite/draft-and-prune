from z3 import *

# Define variables
report = Array('report', IntSort(), IntSort())
solver = Solver()

# Constraint 1 (Domain)
d = Int('d')
t = Int('t')
solver.add(ForAll([d, t], Implies(And(d >= 0, d < 3, t >= 0, t < 2), And(report[d][t] >= 0, report[d][t] < 8))))

# Constraint 2 (Distinctness)
solver.add(Distinct([report[d][t] for d in range(3) for t in range(2)]))

# Constraint 3 (George's schedule)
solver.add(Or(report[1][0] == 0, report[1][1] == 0))
solver.add(And(report[0][0] != 0, report[0][1] != 0, report[2][0] != 0, report[2][1] != 0))

# Constraint 4 (Olivia and Robert's afternoon restriction)
solver.add(And(report[0][1] != 6, report[0][1] != 7, report[1][1] != 6, report[1][1] != 7, report[2][1] != 6, report[2][1] != 7))

# Constraint 5 (Nina's implication)
solver.add(Implies(Or(report[0][0] == 5, report[0][1] == 5), And(Or(report[1][0] == 1, report[1][1] == 1), Or(report[1][0] == 2, report[1][1] == 2))))
solver.add(Implies(Or(report[1][0] == 5, report[1][1] == 5), And(Or(report[2][0] == 1, report[2][1] == 1), Or(report[2][0] == 2, report[2][1] == 2))))

# Constraint 6 (Kyle and Lenore don't report)
solver.add(And([And(report[d][t] != 3, report[d][t] != 4) for d in range(3) for t in range(2)]))

# Check answer choices
options = [
    [1, 0, 5],  # Helen, George, Nina
    [2, 7, 1],  # Irving, Robert, Helen
    [5, 1, 6],  # Nina, Helen, Olivia
    [6, 7, 2],  # Olivia, Robert, Irving
    [7, 0, 1]   # Robert, George, Helen
]

for i, option in enumerate(options):
    solver.push()
    solver.add(And(report[0][0] == option[0], report[1][0] == option[1], report[2][0] == option[2]))
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
