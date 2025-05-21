from z3 import *

# Define variables
report = Array('report', IntSort(), IntSort(), IntSort())

# Create solver
solver = Solver()

# Constraint 1: Domain
d = Int('d')
t = Int('t')
solver.add(ForAll([d, t], Implies(And(d >= 0, d < 3, t >= 0, t < 2), And(report[d][t] >= 0, report[d][t] < 8))))

# Constraint 2: Exactly 2 reports per day
solver.add(ForAll([d], Implies(And(d >= 0, d < 3), Distinct([report[d][t] for t in range(2)]))))

# Constraint 3: Exactly 6 students report
solver.add(Distinct([report[d][t] for d in range(3) for t in range(2)]))

# Constraint 4: George reports only on Tuesday
solver.add(And(Not(Or(report[0][0] == 0, report[0][1] == 0)), Not(Or(report[2][0] == 0, report[2][1] == 0)), Or(report[1][0] == 0, report[1][1] == 0)))

# Constraint 5: Olivia and Robert not in afternoon
solver.add(ForAll([d], Implies(And(d >= 0, d < 3), And(report[d][1] != 6, report[d][1] != 7))))

# Constraint 6: Nina implies Helen and Irving next day, unless Wednesday
solver.add(ForAll([d], Implies(And(d >= 0, d < 2), Implies(Or(report[d][0] == 5, report[d][1] == 5), And(Or(report[d+1][0] == 1, report[d+1][1] == 1), Or(report[d+1][0] == 2, report[d+1][1] == 2))))))

# Constraint 7: Helen, Kyle, and Lenore give morning reports
solver.add(And(Or(report[0][0] == 1, report[1][0] == 1, report[2][0] == 1), Or(report[0][0] == 3, report[1][0] == 3, report[2][0] == 3), Or(report[0][0] == 4, report[1][0] == 4, report[2][0] == 4)))


# Check answer choices
options = [
    Not(report[0][0] == 1),
    Not(Or(report[0][0] == 2, report[0][1] == 2)),
    Not(Or(report[2][0] == 2, report[2][1] == 2)),
    Not(Or(report[1][0] == 3, report[1][1] == 3)),
    Not(Or(report[2][0] == 3, report[2][1] == 3))
]
for i, option in enumerate(options):
    solver.push()
    solver.add(option)
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
