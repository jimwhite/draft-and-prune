from z3 import *

# Variables
report = Array('report', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints
# Constraint 1 (Domain)
solver.add(And([And(report[i] >= 0, report[i] < 8) for i in range(6)]))

# Constraint 2 (Students Reporting)
solver.add(And(Distinct([report[i] for i in range(6)]),
               And([Or(report[i] == 0, report[i] == 1, report[i] == 2, report[i] == 5, report[i] == 6, report[i] == 7) for i in range(6)])))

# Constraint 3 (Two reports per day)
solver.add(And([Distinct([report[i*2], report[i*2+1]]) for i in range(3)]))

# Constraint 4 (George's schedule)
solver.add(And(Or(report[2] == 0, report[3] == 0), report[0] != 0, report[1] != 0, report[4] != 0, report[5] != 0))

# Constraint 5 (Olivia and Robert's schedule)
solver.add(And(report[1] != 6, report[3] != 6, report[5] != 6, report[1] != 7, report[3] != 7, report[5] != 7))

# Constraint 6 (Nina's schedule implication - Mon/Tue)
solver.add(Implies(Or(report[0] == 5, report[1] == 5), And(Or(report[2] == 1, report[3] == 1), Or(report[2] == 2, report[3] == 2))))

# Constraint 7 (Nina's schedule implication - Tue/Wed)
solver.add(Implies(Or(report[2] == 5, report[3] == 5), And(Or(report[4] == 1, report[5] == 1), Or(report[4] == 2, report[5] == 2))))


# Answer Choices
choices = [
    [1, 0, 5],  # Helen, George, Nina
    [2, 7, 1],  # Irving, Robert, Helen
    [5, 1, 6],  # Nina, Helen, Olivia
    [6, 7, 2],  # Olivia, Robert, Irving
    [7, 0, 1]   # Robert, George, Helen
]

for i, choice in enumerate(choices):
    solver.push()
    solver.add(report[0] == choice[0])
    solver.add(report[2] == choice[1])
    solver.add(report[4] == choice[2])
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()