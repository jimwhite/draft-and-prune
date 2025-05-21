from z3 import *

# Define variables
year_assignment = Array('year_assignment', IntSort(), IntSort())

# Create solver
solver = Solver()

# Constraints
i = Int('i')
solver.add(ForAll([i], Implies(And(i >= 0, i <= 3), And(year_assignment[i] >= 0, year_assignment[i] < 6)))) # Constraint 1
solver.add(Distinct([year_assignment[i] for i in range(4)])) # Constraint 2
solver.add(Or(year_assignment[2] == 0, year_assignment[2] == 4)) # Constraint 3
solver.add(Implies(Or([year_assignment[i] == 1 for i in range(4)]), Or(year_assignment[0] == 1, year_assignment[1] == 1))) # Constraint 4
solver.add(Implies(Or([year_assignment[i] == 4 for i in range(4)]), Or([year_assignment[i] == 3 for i in range(4)]))) # Constraint 5
solver.add(And([Implies(year_assignment[i] == 3, year_assignment[i-1] == 2) for i in range(1,4)])) # Constraint 6


# Answer choices
options = [
    [0, 2, 3, 5],  # Louis, Onyx, Ryan, Yoshio
    [1, 5, 4, 2],  # Mollie, Yoshio, Tiffany, Onyx
    [2, 3, 0, 4],  # Onyx, Ryan, Louis, Tiffany
    [4, 2, 0, 3],  # Tiffany, Onyx, Louis, Ryan
    [5, 2, 0, 1]   # Yoshio, Onyx, Louis, Mollie
]

# Check options
for idx, option in enumerate(options):
    solver.push()
    for i in range(4):
        solver.add(year_assignment[i] == option[i])
    if solver.check() == sat:
        print(f"Option {chr(65 + idx)} is correct")
        exit()
    solver.pop()