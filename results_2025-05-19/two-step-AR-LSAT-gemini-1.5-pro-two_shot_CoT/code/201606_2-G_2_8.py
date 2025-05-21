from z3 import *

year_assignment = Array('year_assignment', IntSort(), IntSort())
y = Int('y')
solver = Solver()

# Constraint 1 (Domain)
solver.add(ForAll([y], Implies(And(y >= 0, y < 4), And(year_assignment[y] >= 0, year_assignment[y] < 6))))

# Constraint 2 (Distinctness)
solver.add(Distinct([year_assignment[y] for y in range(4)]))

# Constraint 3 (1923 Assignment)
solver.add(Or(year_assignment[2] == 0, year_assignment[2] == 4))

# Constraint 4 (Mollie's Assignment)
solver.add(Implies(Or([year_assignment[i] == 1 for i in range(4)]), Or(year_assignment[0] == 1, year_assignment[1] == 1)))

# Constraint 5 (Tiffany/Ryan Assignment)
solver.add(Implies(Or([year_assignment[i] == 4 for i in range(4)]), Or([year_assignment[i] == 3 for i in range(4)])))

# Constraint 6-9 (Ryan/Onyx Assignment)
solver.add(Implies(year_assignment[0] == 3, year_assignment[1] == 2))
solver.add(Implies(year_assignment[1] == 3, year_assignment[0] == 2))
solver.add(Implies(year_assignment[2] == 3, year_assignment[1] == 2))
solver.add(Implies(year_assignment[3] == 3, year_assignment[2] == 2))

# Ryan and Yoshio are assigned
solver.add(Or([year_assignment[i] == 3 for i in range(4)]))
solver.add(Or([year_assignment[i] == 5 for i in range(4)]))

answer_choices = [
    (0, year_assignment[2] == 0),  # A: Louis is assigned to 1923
    (1, year_assignment[0] == 1),  # B: Mollie is assigned to 1921
    (2, year_assignment[1] == 2),  # C: Onyx is assigned to 1922
    (3, year_assignment[3] == 4),  # D: Tiffany is assigned to 1924
    (4, year_assignment[1] == 5)   # E: Yoshio is assigned to 1922
]

for i, constraint in answer_choices:
    solver.push()
    solver.add(constraint)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()