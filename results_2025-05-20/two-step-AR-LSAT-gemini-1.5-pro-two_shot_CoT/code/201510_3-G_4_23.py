from z3 import *

# Define variables
season_of_cookbook = Array('season_of_cookbook', IntSort(), IntSort())

# Define constraints
constraints = []

# Constraint 0 (Domain)
for i in range(6):
    constraints.append(And(season_of_cookbook[i] >= 0, season_of_cookbook[i] <= 1))

# Constraint 1 (M and P different seasons)
constraints.append(season_of_cookbook[2] != season_of_cookbook[5])

# Constraint 2 (K and N same season)
constraints.append(season_of_cookbook[0] == season_of_cookbook[3])

# Constraint 3 (K in fall implies O in fall)
constraints.append(Implies(season_of_cookbook[0] == 0, season_of_cookbook[4] == 0))

# Original Constraint 4 (M in fall implies N in spring)
original_constraint = Implies(season_of_cookbook[2] == 0, season_of_cookbook[3] == 1)

# Find all models satisfying original constraints
solver = Solver()
for constraint in constraints:
    solver.add(constraint)
solver.add(original_constraint)

reference_models = []
while solver.check() == sat:
    model = solver.model()
    reference_models.append(model)
    block = []
    for i in range(6):
        # The error was here: model[season_of_cookbook[i]] needs to be accessed as model.eval(season_of_cookbook[i])
        block.append(season_of_cookbook[i] != model.eval(season_of_cookbook[i]))
    solver.add(Or(block))

# Check answer choices
answer_choices = [
    Implies(season_of_cookbook[1] == 0, season_of_cookbook[2] == 1),  # A
    Implies(season_of_cookbook[3] == 0, season_of_cookbook[5] == 0),  # B
    Implies(season_of_cookbook[2] == 1, season_of_cookbook[5] == 0),  # C
    Implies(season_of_cookbook[3] == 1, season_of_cookbook[2] == 1),  # D
    Implies(season_of_cookbook[4] == 1, season_of_cookbook[3] == 1)   # E
]

for i, choice in enumerate(answer_choices):
    solver = Solver()
    for constraint in constraints:
        solver.add(constraint)
    solver.add(choice)
    
    current_models = []
    while solver.check() == sat:
        model = solver.model()
        current_models.append(model)
        block = []
        for j in range(6):
            # Fix the same error here
            block.append(season_of_cookbook[j] != model.eval(season_of_cookbook[j]))
        solver.add(Or(block))

    if set(str(m) for m in current_models) == set(str(m) for m in reference_models):
        print(f"Option {chr(65 + i)} is correct")
        exit()
