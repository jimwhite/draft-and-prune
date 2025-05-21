from z3 import *

# Define cargo type constants
F, G, L, M, P, T = Ints('F G L M P T')

# Define the bay_cargo array
bay_cargo = Array('bay_cargo', IntSort(), IntSort())

# Define integer variables for quantifiers
i = Int('i')
j = Int('j')

# Create a Z3 solver
solver = Solver()

# Constraint 0: Domain
solver.add(ForAll([i], Implies(And(i >= 1, i <= 6), And(bay_cargo[i] >= 0, bay_cargo[i] <= 5))))

# Constraint 1: Distinctness
solver.add(Distinct([bay_cargo[k] for k in range(1, 7)]))

# Constraint 2: Grain > Livestock
solver.add(ForAll([i, j], Implies(And(bay_cargo[i] == G, bay_cargo[j] == L), i > j)))

# Constraint 3: Livestock > Textiles
solver.add(ForAll([i, j], Implies(And(bay_cargo[i] == L, bay_cargo[j] == T), i > j)))

# Constraint 4: Produce > Fuel
solver.add(ForAll([i, j], Implies(And(bay_cargo[i] == P, bay_cargo[j] == F), i > j)))

# Constraint 5: Textiles next to Produce
solver.add(ForAll([i], Implies(And(i >= 1, i <= 5), Or(And(bay_cargo[i] == T, bay_cargo[i+1] == P), And(bay_cargo[i] == P, bay_cargo[i+1] == T)))))

# Constraint 6: Machinery and Grain separated by one bay
solver.add(ForAll([i, j], Implies(And(bay_cargo[i] == M, bay_cargo[j] == G), Or(i == j + 2, j == i + 2))))

# Add constraints to fix the cargo types to integer values
solver.add(And(F == 0, G == 1, L == 2, M == 3, P == 4, T == 5))


# Determine the number of bays with completely determined cargo
determined_bays_count = 0
for b in range(1, 7):
    solver.push()
    if solver.check() == sat:  # Check base constraints are consistent
        m = solver.model()
        predicted_cargo_id = m.eval(bay_cargo[b])
        solver.add(bay_cargo[b] != predicted_cargo_id)
        if solver.check() == unsat:
            determined_bays_count += 1
    solver.pop()

# Map count to answer choices
answers = ["two", "three", "four", "five", "six"]
if 0 <= determined_bays_count < len(answers):
    print(f"Option {chr(65 + determined_bays_count)} is correct")
    exit()

