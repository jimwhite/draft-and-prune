from z3 import *

year_assignment = Array('year_assignment', IntSort(), IntSort())
y = Int('y')
solver = Solver()

# Constraint 1 (Domain)
solver.add(ForAll([y], And(year_assignment[y] >= 0, year_assignment[y] < 6)))

# Constraint 2 (Distinctness)
solver.add(Distinct([year_assignment[i] for i in range(4)]))

# Constraint 3 (1923 Assignment)
solver.add(Or(year_assignment[2] == 0, year_assignment[2] == 4))

# Constraint 4 (Mollie's Assignment)
solver.add(Implies(Or([year_assignment[i] == 1 for i in range(4)]), Or(year_assignment[0] == 1, year_assignment[1] == 1)))

# Constraint 5 (Tiffany/Ryan Assignment)
solver.add(Implies(Or([year_assignment[i] == 4 for i in range(4)]), Or([year_assignment[i] == 3 for i in range(4)])))

# Constraint 6-8 (Ryan/Onyx Assignment)
solver.add(Implies(year_assignment[1] == 3, year_assignment[0] == 2))
solver.add(Implies(year_assignment[2] == 3, year_assignment[1] == 2))
solver.add(Implies(year_assignment[3] == 3, year_assignment[2] == 2))

# Constraint 9 (Ryan not in 1921):
solver.add(year_assignment[0] != 3)


# Premise: Ryan and Yoshio are assigned
solver.add(Or([year_assignment[i] == 3 for i in range(4)]))
solver.add(Or([year_assignment[i] == 5 for i in range(4)]))

answer_choices = [
    (year_assignment[2] == 0),  # A
    (year_assignment[0] == 1),  # B
    (year_assignment[1] == 2),  # C
    (year_assignment[3] == 4),  # D
    (year_assignment[1] == 5),  # E
]

for i, choice in enumerate(answer_choices):
    solver.push()
    solver.add(choice)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()