from z3 import *

# Define the number of companies and resources
NUM_COMPANIES = 3
NUM_RESOURCES = 2

# Create a 2D array to represent target_days
target_days = [[Int(f"target_days[{c}][{r}]") for r in range(NUM_RESOURCES)] for c in range(NUM_COMPANIES)]

# Create solver
solver = Solver()

# Constraint 1: Domain of target_days
for c in range(NUM_COMPANIES):
    for r in range(NUM_RESOURCES):
        solver.add(target_days[c][r] >= 1, target_days[c][r] <= 3)

# Constraint 2: Website target not longer than voicemail target
for c in range(NUM_COMPANIES):
    solver.add(target_days[c][0] <= target_days[c][1])

# Constraint 3: Image's voicemail target shorter than others
for c in range(NUM_COMPANIES):
    if c != 0:
        solver.add(target_days[0][1] < target_days[c][1])

# Constraint 4: Solide's website target shorter than Truvest's
solver.add(target_days[1][0] < target_days[2][0])

# Constraint 5: Image's website target is 2 days
solver.add(target_days[0][0] == 2)

# Answer choices
options = [
    "Image's voicemail target",
    "Solide's website target",
    "Solide's voicemail target",
    "Truvest's website target",
    "Truvest's voicemail target"
]
option_constraints = [
    target_days[0][1] != 2,
    target_days[1][0] != 2,
    target_days[1][1] != 2,
    target_days[2][0] != 2,
    target_days[2][1] != 2
]

# Check each answer choice
for i in range(len(options)):
    solver.push()
    solver.add(option_constraints[i])
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()

