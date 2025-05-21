from z3 import *

# Variables
bay_cargo = Array('bay_cargo', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints
i = Int('i')
j = Int('j')

# Constraint 0: Domain of bay_cargo
solver.add(ForAll(i, Implies(And(i >= 1, i <= 6), And(bay_cargo[i] >= 0, bay_cargo[i] <= 5))))

# Constraint 1: Distinctness of cargo assignments
solver.add(Distinct([bay_cargo[k] for k in range(1, 7)]))

# Constraint 2: Grain > Livestock
solver.add(ForAll([i, j], Implies(And(bay_cargo[i] == 1, bay_cargo[j] == 2, i >= 1, i <= 6, j >= 1, j <= 6), i > j)))

# Constraint 3: Livestock > Textiles
solver.add(ForAll([i, j], Implies(And(bay_cargo[i] == 2, bay_cargo[j] == 5, i >= 1, i <= 6, j >= 1, j <= 6), i > j)))

# Constraint 4: Produce > Fuel
solver.add(ForAll([i, j], Implies(And(bay_cargo[i] == 4, bay_cargo[j] == 0, i >= 1, i <= 6, j >= 1, j <= 6), i > j)))

# Constraint 5: Textiles next to Produce
solver.add(Exists(i, Implies(And(i >= 1, i <= 5), Or(And(bay_cargo[i] == 5, bay_cargo[i+1] == 4), And(bay_cargo[i+1] == 5, bay_cargo[i] == 4)))))


# Check answer choices
answer_choices = [
    "The bay holding fuel is next to the bay holding machinery.",
    "The bay holding grain is next to the bay holding machinery.",
    "The bay holding livestock is next to the bay holding fuel.",
    "The bay holding produce is next to the bay holding livestock.",
    "The bay holding textiles is next to the bay holding fuel."
]

for idx, choice in enumerate(answer_choices):
    solver.push()
    if idx == 0:  # A
        solver.add(ForAll([i, j], Implies(And(bay_cargo[i] == 0, bay_cargo[j] == 3, i >= 1, i <= 6, j >= 1, j <= 6), Not(Or(i == j+1, j == i+1)))))
    elif idx == 1:  # B
        solver.add(ForAll([i, j], Implies(And(bay_cargo[i] == 1, bay_cargo[j] == 3, i >= 1, i <= 6, j >= 1, j <= 6), Not(Or(i == j+1, j == i+1)))))
    elif idx == 2:  # C
        solver.add(ForAll([i, j], Implies(And(bay_cargo[i] == 2, bay_cargo[j] == 0, i >= 1, i <= 6, j >= 1, j <= 6), Not(Or(i == j+1, j == i+1)))))
    elif idx == 3:  # D
        solver.add(ForAll([i, j], Implies(And(bay_cargo[i] == 4, bay_cargo[j] == 2, i >= 1, i <= 6, j >= 1, j <= 6), Not(Or(i == j+1, j == i+1)))))
    elif idx == 4:  # E
        solver.add(ForAll([i, j], Implies(And(bay_cargo[i] == 5, bay_cargo[j] == 0, i >= 1, i <= 6, j >= 1, j <= 6), Not(Or(i == j+1, j == i+1)))))

    if solver.check() == unsat:
        print(f"Option {chr(65 + idx)} is correct")
        exit()
    solver.pop()