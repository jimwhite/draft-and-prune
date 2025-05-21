from z3 import *

# Define variables
year_assignment = Array('year_assignment', IntSort(), IntSort())
assigned = Array('assigned', IntSort(), BoolSort())

# Define solver
solver = Solver()

# Constraints
y = Int('y')
s = Int('s')

# Constraint 0: Domain of year_assignment
solver.add(ForAll([y], Implies(And(y >= 0, y < 4), And(year_assignment[y] >= 0, year_assignment[y] < 6))))

# Constraint 1: Unique year assignments
solver.add(Distinct([year_assignment[i] for i in range(4)]))

# Constraint 2: 1923 assignment
solver.add(Or(year_assignment[2] == 0, year_assignment[2] == 4))

# Constraint 3: Mollie's assignment
solver.add(Implies(assigned[1], Or(year_assignment[0] == 1, year_assignment[1] == 1)))

# Constraint 4: Tiffany and Ryan
solver.add(Implies(assigned[4], assigned[3]))

# Constraint 5: Ryan and Onyx
solver.add(Implies(assigned[3], Exists([y], And(year_assignment[y] == 3, year_assignment[y-1] == 2, y >= 1, y <= 3))))

# Constraint 6: Assigned means assigned
solver.add(ForAll([s], Implies(And(s >= 0, s < 6), assigned[s] == Or([year_assignment[y] == s for y in range(4)]))))


# Define conditions and choices
mollie_in_1922 = (year_assignment[1] == 1)
not_mollie_in_1922 = Not(mollie_in_1922)

choice_A = (year_assignment[3] == 0)
choice_B = (year_assignment[0] == 2)
choice_C = (year_assignment[3] == 2)
choice_D = (year_assignment[2] == 4)
choice_E = (year_assignment[0] == 5)

choices = [choice_A, choice_B, choice_C, choice_D, choice_E]
choice_letters = ['A', 'B', 'C', 'D', 'E']

# Check each choice
for choice, letter in zip(choices, choice_letters):
    temp_solver = Solver()
    temp_solver.add(solver.assertions())
    temp_solver.add(choice)
    temp_solver.add(not_mollie_in_1922)
    if temp_solver.check() == unsat:
        print(f"Option {letter} is correct")
        exit()