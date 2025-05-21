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

# Constraint 6 (Ryan/Onyx Assignment)
solver.add(Implies(And(Or([year_assignment[i] == 3 for i in range(1,4)]), Not(year_assignment[0] == 3)), Or([And(year_assignment[i] == 3, year_assignment[i-1] == 2) for i in range(1,4)])))

# Constraint 7 (Yoshio Not Assigned)
solver.add(Not(Or([year_assignment[i] == 5 for i in range(4)])))

answer_choices = [
    Not(Or([year_assignment[i] == 0 for i in range(4)])),  # A
    Not(Or([year_assignment[i] == 3 for i in range(4)])),  # B
    Not(Or([year_assignment[i] == 4 for i in range(4)])),  # C
    year_assignment[1] == 2,  # D
    year_assignment[3] == 0   # E
]

for i in range(len(answer_choices)):
    solver.push()
    solver.add(answer_choices[i])
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()