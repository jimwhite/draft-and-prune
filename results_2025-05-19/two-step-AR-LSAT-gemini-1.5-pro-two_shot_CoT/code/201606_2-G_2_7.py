from z3 import *

# Variables
year_assignment = Array('year_assignment', IntSort(), IntSort())
y = Int('y')

# Solver and base constraints
solver = Solver()

# Constraint 0 (Domain)
solver.add(ForAll([y], Implies(And(y >= 0, y < 4), And(year_assignment[y] >= 0, year_assignment[y] <= 5))))

# Constraint 1 (Distinctness)
solver.add(Distinct([year_assignment[y] for y in range(4)]))

# Constraint 2 (1923 Assignment)
solver.add(Or(year_assignment[2] == 0, year_assignment[2] == 4))

# Constraint 3 (Mollie's Assignment)
solver.add(Implies(Or([year_assignment[y] == 1 for y in range(4)]), Or(year_assignment[0] == 1, year_assignment[1] == 1)))

# Constraint 4 (Tiffany and Ryan)
solver.add(Implies(Or([year_assignment[y] == 4 for y in range(4)]), Or([year_assignment[y] == 3 for y in range(4)])))

# Constraint 5 (Ryan and Onyx)
solver.add(ForAll([y], Implies(And(y >= 0, y < 3, year_assignment[y+1] == 3), year_assignment[y] == 2)))

# Answer choices and checking
answer_choices = [
    (3, 0),  # A: Louis is assigned to 1924
    (0, 2),  # B: Onyx is assigned to 1921
    (3, 2),  # C: Onyx is assigned to 1924
    (2, 4),  # D: Tiffany is assigned to 1923
    (0, 5)   # E: Yoshio is assigned to 1921
]

for i, (year, student) in enumerate(answer_choices):
    solver.push()
    solver.add(year_assignment[year] == student)
    solver.add(year_assignment[1] != 1)  # Mollie is NOT assigned to 1922
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()