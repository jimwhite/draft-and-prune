from z3 import *

# Cargo types: fuel=0, grain=1, livestock=2, machinery=3, produce=4, textiles=5
cargo_types = ["fuel", "grain", "livestock", "machinery", "produce", "textiles"]

# Position variables: pos[type] = bay number (1-6)
pos = {t: Int(f"pos_{t}") for t in cargo_types}

# Base solver
solver = Solver()

# Domain constraints: positions 1-6
for t in cargo_types:
    solver.add(pos[t] >= 1, pos[t] <= 6)

# Distinctness constraint: all positions are different
solver.add(Distinct(*[pos[t] for t in cargo_types]))

# Ordering constraints
solver.add(pos["grain"] > pos["livestock"])
solver.add(pos["livestock"] > pos["textiles"])
solver.add(pos["produce"] > pos["fuel"])

# Adjacency constraint: textiles and produce are adjacent
solver.add(Or(pos["produce"] == pos["textiles"] + 1, pos["produce"] == pos["textiles"] - 1))

# Conditional constraint: exactly one bay between machinery and grain
solver.add(Or(pos["grain"] == pos["machinery"] + 2, pos["grain"] == pos["machinery"] - 2))

# Collect all solutions
solutions = []
while solver.check() == sat:
    model = solver.model()
    solution = [model.eval(pos[t]).as_long() for t in cargo_types]
    solutions.append(solution)
    
    # Add constraint to exclude current solution
    solver.add(Or(*[pos[t] != val for t, val in zip(cargo_types, solution)]))

# Find positions that are fixed across all solutions
if solutions:
    # For each cargo type, collect all positions it takes in the solutions
    fixed_positions = []
    for i in range(6):
        positions = set(sol[i] for sol in solutions)
        if len(positions) == 1:
            fixed_positions.append(True)
        else:
            fixed_positions.append(False)
    
    # Count how many cargo types have fixed positions
    count_fixed = sum(fixed_positions)
    
    # Map to answer choices
    if count_fixed == 2:
        print("two")
    elif count_fixed == 3:
        print("three")
    elif count_fixed == 4:
        print("four")
    elif count_fixed == 5:
        print("five")
    else:  # count_fixed == 6
        print("six")
else:
    # No solutions exist (shouldn't happen for a valid problem)
    print("none")