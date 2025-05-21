from z3 import *

# Variables
year_assignment = Array('year_assignment', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints
y = Int('y')  # Declare y for ForAll
solver.add(ForAll([y], Implies(And(y >= 0, y < 4), And(year_assignment[y] >= 0, year_assignment[y] < 6)))) # Constraint 1
solver.add(Distinct([year_assignment[y] for y in range(4)])) # Constraint 2
solver.add(Or(year_assignment[2] == 0, year_assignment[2] == 4)) # Constraint 3
solver.add(Implies(Or([year_assignment[y] == 1 for y in range(4)]), Or(year_assignment[0] == 1, year_assignment[1] == 1))) # Constraint 4
solver.add(Implies(Or([year_assignment[y] == 4 for y in range(4)]), Or([year_assignment[y] == 3 for y in range(4)]))) # Constraint 5
solver.add(And(Implies(year_assignment[1] == 3, year_assignment[0] == 2), Implies(year_assignment[2] == 3, year_assignment[1] == 2), Implies(year_assignment[3] == 3, year_assignment[2] == 2))) # Constraint 6


# Count possible students for 1921
count = 0
for s in range(6):
    solver.push()
    solver.add(year_assignment[0] == s)
    if solver.check() == sat:
        count += 1
    solver.pop()

# Check answer choices
answers = ["six", "five", "four", "three", "two"]
if count == 2:
    print("Option E is correct")
elif count == 3:
    print("Option D is correct")
elif count == 4:
    print("Option C is correct")
elif count == 5:
    print("Option B is correct")
elif count == 6:
    print("Option A is correct")