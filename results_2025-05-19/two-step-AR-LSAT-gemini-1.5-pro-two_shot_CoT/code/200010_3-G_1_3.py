from z3 import *

# Variables
report = [[Int(f"report_{d}_{t}") for t in range(2)] for d in range(3)]

# Solver
solver = Solver()

# Constraints

# Constraint 1: Exactly two reports per day
for d in range(3):
    solver.add(Distinct(report[d]))

# Constraint 2: Exactly six students give reports
reports_list = [report[d][t] for d in range(3) for t in range(2)]
solver.add(Distinct(reports_list))

# Generate all combinations of 7 students
from itertools import combinations

for missing_students in combinations(range(8), 2):
    clause = []
    for d in range(3):
        for t in range(2):
            for student in missing_students:
                clause.append(report[d][t] != student)
    solver.add(Or(clause))


# Constraint 3: George reports only on Tuesday
solver.add(Or(report[1][0] == 0, report[1][1] == 0))
solver.add(And(report[0][0] != 0, report[0][1] != 0, report[2][0] != 0, report[2][1] != 0))

# Constraint 4: Olivia and Robert do not give afternoon reports
for d in range(3):  # Fixed: Iterate over days and add constraints individually
    solver.add(report[d][1] != 6)
    solver.add(report[d][1] != 7)


# Constraint 5: Nina's report implies Helen and Irving report the next day, unless Wednesday
for d in range(3):
    solver.add(Implies(Or(report[d][0] == 5, report[d][1] == 5),
                         If(d < 2,
                            And(Or(report[d+1][0] == 1, report[d+1][1] == 1),
                                Or(report[d+1][0] == 2, report[d+1][1] == 2)),
                            True)))


# Answer Choices
options = [
    (0, 4),  # George and Lenore
    (1, 5),  # Helen and Nina
    (2, 7),  # Irving and Robert
    (3, 5),  # Kyle and Nina
    (6, 3)   # Olivia and Kyle
]

for i, (s1, s2) in enumerate(options):
    solver.push()
    same_day = Or(And(Or(report[0][0] == s1, report[0][1] == s1), Or(report[0][0] == s2, report[0][1] == s2)),
                 And(Or(report[1][0] == s1, report[1][1] == s1), Or(report[1][0] == s2, report[1][1] == s2)),
                 And(Or(report[2][0] == s1, report[2][1] == s1), Or(report[2][0] == s2, report[2][1] == s2)))

    not_wednesday = Not(And(Or(report[2][0] == s1, report[2][1] == s1), Or(report[2][0] == s2, report[2][1] == s2)))
    solver.add(And(same_day, not_wednesday))

    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
