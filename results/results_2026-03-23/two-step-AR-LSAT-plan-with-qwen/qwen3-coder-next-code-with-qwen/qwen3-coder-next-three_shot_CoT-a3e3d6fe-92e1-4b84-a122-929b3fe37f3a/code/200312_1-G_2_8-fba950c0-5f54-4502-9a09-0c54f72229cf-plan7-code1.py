from z3 import *

# Cargo types: fuel=0, grain=1, livestock=2, machinery=3, produce=4, textiles=5
cargo_types = ["fuel", "grain", "livestock", "machinery", "produce", "textiles"]

# bay[i] = bay number (1-6) for cargo type i
bay = [Int(f"bay_{i}") for i in range(6)]

solver = Solver()

# Domain constraints: each bay number between 1 and 6, all distinct
solver.add(Distinct(bay))
for i in range(6):
    solver.add(bay[i] >= 1, bay[i] <= 6)

# Ordering constraints
solver.add(bay[1] > bay[2])      # grain > livestock
solver.add(bay[2] > bay[5])      # livestock > textiles
solver.add(bay[4] > bay[0])      # produce > fuel

# Textiles and produce are adjacent
solver.add(Or(bay[4] == bay[5] + 1, bay[5] == bay[4] + 1))

# Extra condition: exactly one bay between machinery and grain
solver.add(Or(bay[1] == bay[3] + 2, bay[3] == bay[1] + 2))

# Collect all solutions
solutions = []
while solver.check() == sat:
    model = solver.model()
    # Record assignment
    assignment = [model.eval(bay[i]).as_long() for i in range(6)]
    solutions.append(assignment)
    
    # Add constraint to exclude current solution
    solver.add(Or(*[bay[i] != assignment[i] for i in range(6)]))

# Build mapping: bay_number -> set of cargo types that appear there across all solutions
bay_to_types = {b: set() for b in range(1, 7)}
for assignment in solutions:
    for cargo_type_idx in range(6):
        bay_num = assignment[cargo_type_idx]
        bay_to_types[bay_num].add(cargo_type_idx)

# Count how many bays have exactly one possible cargo type
fixed_bays = sum(1 for b in range(1, 7) if len(bay_to_types[b]) == 1)

# Map to answer string
answer_map = {2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six'}
print(answer_map[fixed_bays])