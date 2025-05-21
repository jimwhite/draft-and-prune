from z3 import *

# Define variables
assigned = Array('assigned', IntSort(), IntSort())
p = Int('p')

# Define base constraints
base_constraints = [
    ForAll([p], And(assigned[p] >= 0, assigned[p] <= 2)),
    sum([If(assigned[p] == 0, 1, 0) for p in range(6)]) >= 2,
    sum([If(assigned[p] == 1, 1, 0) for p in range(6)]) >= 2,
    And(assigned[0] == assigned[2], assigned[0] != 2),
    Implies(And(assigned[4] != 2, assigned[5] != 2), assigned[4] != assigned[5]),
    Implies(assigned[1] == 0, assigned[4] == 1)
]

# Define original constraint
original_constraint = Implies(assigned[3] != 1, And(assigned[2] == 1, assigned[5] == 1))

# Define answer choice constraints
choice_constraints = [
    Implies(assigned[3] == 0, Not(And(assigned[2] == 0, assigned[5] == 0))),
    Implies(assigned[3] == 0, assigned[4] == 0),
    Implies(assigned[3] != 1, And(assigned[0] == 1, assigned[5] == 1)),
    Implies(assigned[3] != 1, assigned[2] != assigned[4]),
    Implies(Not(Or(assigned[2] == 1, assigned[5] == 1)), assigned[3] == 1)
]

# Get original models
solver = Solver()
solver.add(base_constraints)
solver.add(original_constraint)
original_models = []
while solver.check() == sat:
    model = solver.model()
    original_models.append(model)
    blocking_clause = Or([assigned[i] != model[assigned[i]].as_long() for i in range(6)])
    solver.add(blocking_clause)

# Check each answer choice
for i, choice_constraint in enumerate(choice_constraints):
    solver = Solver() # Fixed: Create a new solver instance for each choice
    solver.add(base_constraints)
    solver.add(choice_constraint)
    choice_models = []
    while solver.check() == sat:
        model = solver.model()
        choice_models.append(model)
        blocking_clause = Or([assigned[j] != model[assigned[j]].as_long() for j in range(6)])
        solver.add(blocking_clause)

    if len(original_models) == len(choice_models) and all(any(m1 == m2 for m2 in choice_models) for m1 in original_models):
        print(f"Option {chr(65 + i)} is correct")
        exit()
