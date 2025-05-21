from z3 import *

# Define variables
day1_assignments = Array('day1_assignments', IntSort(), IntSort())
day2_assignments = Array('day2_assignments', IntSort(), IntSort())
riders = [0, 1, 2, 3]  # R, S, T, Y
bicycles = [0, 1, 2, 3]  # F, G, H, J

# Create solver and add constraints
solver = Solver()

# Constraint 1: Domain
for r in riders:
    solver.add(And(day1_assignments[r] >= 0, day1_assignments[r] < 4))
    solver.add(And(day2_assignments[r] >= 0, day2_assignments[r] < 4))

# Constraint 2: Distinct Bikes per Day
solver.add(Distinct([day1_assignments[r] for r in riders]))
solver.add(Distinct([day2_assignments[r] for r in riders]))

# Constraint 3: Distinct Bikes per Rider Across Days
for r in riders:
    solver.add(day1_assignments[r] != day2_assignments[r])

# Constraint 4: Reynaldo cannot test F
solver.add(And(day1_assignments[0] != 0, day2_assignments[0] != 0))

# Constraint 5: Yuki cannot test J
solver.add(And(day1_assignments[3] != 3, day2_assignments[3] != 3))

# Constraint 6: Theresa tests H
solver.add(Xor(day1_assignments[2] == 2, day2_assignments[2] == 2))

# Constraint 7: Yuki's Day 1 bike is Seamus's Day 2 bike
solver.add(day1_assignments[3] == day2_assignments[1])

# Check answer choices
answer_choices = [
    ("Both Reynaldo and Seamus test J.",
     And(Or(day1_assignments[0] == 3, day2_assignments[0] == 3), Or(day1_assignments[1] == 3, day2_assignments[1] == 3))),
    ("Both Reynaldo and Theresa test J.",
     And(Or(day1_assignments[0] == 3, day2_assignments[0] == 3), Or(day1_assignments[2] == 3, day2_assignments[2] == 3))),
    ("Both Reynaldo and Yuki test G.",
     And(Or(day1_assignments[0] == 1, day2_assignments[0] == 1), Or(day1_assignments[3] == 1, day2_assignments[3] == 1))),
    ("Both Seamus and Theresa test G.",
     And(Or(day1_assignments[1] == 1, day2_assignments[1] == 1), Or(day1_assignments[2] == 1, day2_assignments[2] == 1))),
    ("Both Theresa and Yuki test F.",
     And(Or(day1_assignments[2] == 0, day2_assignments[2] == 0), Or(day1_assignments[3] == 0, day2_assignments[3] == 0)))
]

for i, (description, constraint) in enumerate(answer_choices):
    solver.push()
    solver.add(constraint)
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()