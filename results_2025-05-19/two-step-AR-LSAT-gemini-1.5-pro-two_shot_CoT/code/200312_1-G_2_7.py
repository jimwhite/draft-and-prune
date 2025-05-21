from z3 import *

# Variables
bay_cargo = Array('bay_cargo', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints

# Constraint 0 (Domain)
i = Int('i')
solver.add(ForAll([i], Implies(And(i >= 1, i <= 6), And(bay_cargo[i] >= 0, bay_cargo[i] <= 5))))

# Constraint 1 (Distinctness)
solver.add(Distinct([bay_cargo[i] for i in range(1, 7)]))

# Constraint 2 (Grain > Livestock)
i = Int('i')
j = Int('j')
solver.add(ForAll([i, j], Implies(And(bay_cargo[i] == 1, bay_cargo[j] == 2), i > j)))

# Constraint 3 (Livestock > Textiles)
i = Int('i')
j = Int('j')
solver.add(ForAll([i, j], Implies(And(bay_cargo[i] == 2, bay_cargo[j] == 5), i > j)))

# Constraint 4 (Produce > Fuel)
i = Int('i')
j = Int('j')
solver.add(ForAll([i, j], Implies(And(bay_cargo[i] == 4, bay_cargo[j] == 0), i > j)))

# Constraint 5 (Textiles next to Produce)
i = Int('i')
solver.add(Or(Exists([i], And(i >= 1, i <= 5, bay_cargo[i] == 5, bay_cargo[i+1] == 4)), Exists([i], And(i >= 2, i <= 6, bay_cargo[i] == 5, bay_cargo[i-1] == 4))))


# Answer Choices and their corresponding IDs
answer_choices = ["grain", "livestock", "machinery", "produce", "textiles"]
answer_choice_ids = [1, 2, 3, 4, 5]

# Check each answer choice
for choice_index, choice_id in enumerate(answer_choice_ids):
    solver.push()
    solver.add(bay_cargo[4] == choice_id)
    if solver.check() == unsat:
        print(f"Option {chr(65 + choice_index)} is correct")
        exit()
    solver.pop()