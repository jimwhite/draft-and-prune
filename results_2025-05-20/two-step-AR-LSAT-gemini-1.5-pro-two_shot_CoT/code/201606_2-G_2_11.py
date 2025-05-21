from z3 import *

# Define variables
year_assignment = Array('year_assignment', IntSort(), IntSort())
y = Int('y')

# Create solver and add constraints
solver = Solver()

# Constraint 1: Domain
solver.add(ForAll([y], Implies(And(y >= 0, y < 4), And(year_assignment[y] >= 0, year_assignment[y] < 6))))

# Constraint 2: Distinctness
solver.add(Distinct([year_assignment[i] for i in range(4)]))

# Constraint 3: 1923 Assignment
solver.add(Or(year_assignment[2] == 0, year_assignment[2] == 4))

# Constraint 4: Mollie's Assignment
solver.add(Implies(Or([year_assignment[i] == 1 for i in range(4)]), Or(year_assignment[0] == 1, year_assignment[1] == 1)))

# Constraint 5: Tiffany and Ryan
solver.add(Implies(Or([year_assignment[i] == 4 for i in range(4)]), Or([year_assignment[i] == 3 for i in range(4)])))

# Constraint 6: Ryan and Onyx
solver.add(ForAll([y], Implies(And(y > 0, y < 4, year_assignment[y] == 3), year_assignment[y - 1] == 2)))

# Check answer choices
students = ["Louis", "Mollie", "Onyx", "Ryan", "Yoshio"]
student_ids = [0, 1, 2, 3, 5]

for i, student_id in enumerate(student_ids):
    solver.push()
    solver.add(year_assignment[1] == student_id)
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()