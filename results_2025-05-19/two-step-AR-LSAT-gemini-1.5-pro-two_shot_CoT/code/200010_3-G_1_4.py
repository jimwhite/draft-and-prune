from z3 import *

# Define variables
report = [[Int('report_%s_%s' % (d, t)) for t in range(2)] for d in range(3)]

# Create solver
solver = Solver()

# Constraint 1: Domain
for d in range(3):
    for t in range(2):
        solver.add(report[d][t] >= 0, report[d][t] < 8)

# Constraint 2: Two reports per day
for d in range(3):
    solver.add(Distinct(report[d][0], report[d][1]))

# Constraint 3: Six total reports
solver.add(Distinct([report[d][t] for d in range(3) for t in range(2)]))

# Constraint 4: George on Tuesday
solver.add(Or(report[1][0] == 0, report[1][1] == 0))

# Constraint 5: No Olivia/Robert in afternoon
for d in range(3):
    solver.add(report[d][1] != 6, report[d][1] != 7)

# Constraint 6: Nina implies Helen/Irving next day
for d in range(2):
    solver.add(Implies(Or(report[d][0] == 5, report[d][1] == 5), And(Or(report[d+1][0] == 1, report[d+1][1] == 1), Or(report[d+1][0] == 2, report[d+1][1] == 2))))

# George, Nina, Robert on different days
reports = [0, 5, 7]
for r in reports:
    solver.add(Or([report[d][t] == r for d in range(3) for t in range(2)])) # Corrected: Use Or to ensure at least one assignment

for i in range(3):
    for j in range(2):
        for p in reports:
            for k in range(3):
                for l in range(2):
                    if k != i:
                        solver.add(Implies(report[i][j] == p, Not(report[k][l] == p)))


# Check answer choices
options = [
    Or(report[2][0] == 1, report[2][1] == 1),  # Helen gives a report on Wednesday
    Or(report[0][0] == 5, report[0][1] == 5),  # Nina gives a report on Monday
    Or(report[1][0] == 5, report[1][1] == 5),  # Nina gives a report on Tuesday
    Or(report[0][0] == 6, report[0][1] == 6),  # Olivia gives a report on Monday
    Or(report[2][0] == 7, report[2][1] == 7)   # Robert gives a report on Wednesday
]

for i, option in enumerate(options):
    solver.push()
    solver.add(option)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()

