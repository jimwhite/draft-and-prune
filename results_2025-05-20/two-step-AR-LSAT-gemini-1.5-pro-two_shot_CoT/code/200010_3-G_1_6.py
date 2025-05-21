from z3 import *

# Define variables
report = Array('report', IntSort(), IntSort(), IntSort())
gives_report = Array('gives_report', IntSort(), BoolSort())

solver = Solver()

# Constraint 1: Exactly 6 students give reports
solver.add(PbEq([(gives_report[i], 1) for i in range(8)], 6))

# Constraint 2: All 6 report slots are filled by distinct students
solver.add(Distinct([report[d][t] for d in range(3) for t in range(2)]))

# Constraint 3: Students filling slots are exactly those who give reports
s = Int('s')
solver.add(ForAll([s], gives_report[s] == Exists([d, t], report[d][t] == s)))

# Constraint 4: George's schedule
solver.add(ForAll([d, t], Implies(report[d][t] == 0, d == 1)))

# Constraint 5: Olivia and Robert's schedule
solver.add(ForAll([d], And(report[d][1] != 6, report[d][1] != 7)))

# Constraint 6: Nina's influence
solver.add(ForAll([d, t], Implies(And(report[d][t] == 5, d < 2), Or(
    And(report[d+1][0] == 1, report[d+1][1] == 2),
    And(report[d+1][1] == 1, report[d+1][0] == 2)
))))


# Question constraint: Helen, Kyle, and Lenore give morning reports
solver.add(Or(
    And(report[0][0] == 1, report[1][0] == 3, report[2][0] == 4),
    And(report[0][0] == 1, report[1][0] == 4, report[2][0] == 3),
    And(report[0][0] == 3, report[1][0] == 1, report[2][0] == 4),
    And(report[0][0] == 3, report[1][0] == 4, report[2][0] == 1),
    And(report[0][0] == 4, report[1][0] == 1, report[2][0] == 3),
    And(report[0][0] == 4, report[1][0] == 3, report[2][0] == 1)
))

# Check answer choices
negations = [
    report[0][0] != 1,  # A
    report[0][0] != 2,  # B
    report[2][0] != 2,  # C
    report[1][0] != 3,  # D
    report[2][0] != 3   # E
]

for i, negation in enumerate(negations):
    solver.push()
    solver.add(negation)
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
