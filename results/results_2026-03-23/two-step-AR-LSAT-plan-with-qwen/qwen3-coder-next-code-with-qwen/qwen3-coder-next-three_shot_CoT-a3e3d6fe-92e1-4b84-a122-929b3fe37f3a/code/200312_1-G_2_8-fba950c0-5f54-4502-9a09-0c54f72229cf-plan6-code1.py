from z3 import *

# Cargo type indices: 0-fuel, 1-grain, 2-livestock, 3-machinery, 4-produce, 5-textiles
FUEL, GRAIN, LIVESTOCK, MACHINERY, PRODUCE, TEXTILES = range(6)

# bay[type] = bay number (1-6) where that cargo type is held
bay = [Int(f"bay_{t}") for t in range(6)]

# Base solver
solver = Solver()

# Domain constraints: each bay number between 1 and 6, all distinct
solver.add(Distinct(*bay))
for t in range(6):
    solver.add(bay[t] >= 1, bay[t] <= 6)

# Ordering constraints
solver.add(bay[GRAIN] > bay[LIVESTOCK])
solver.add(bay[LIVESTOCK] > bay[TEXTILES])
solver.add(bay[PRODUCE] > bay[FUEL])

# Textiles and produce are adjacent
solver.add(Or(bay[TEXTILES] == bay[PRODUCE] + 1, bay[TEXTILES] == bay[PRODUCE] - 1))

# Conditional constraint: exactly one bay between machinery and grain
solver.add(Or(bay[MACHINERY] == bay[GRAIN] + 2, bay[MACHINERY] == bay[GRAIN] - 2))

# Collect all satisfying assignments
models = []
while solver.check() == sat:
    m = solver.model()
    models.append([m[bay[t]].as_long() for t in range(6)])
    # Add constraint to exclude current model
    solver.add(Or(*[bay[t] != models[-1][t] for t in range(6)]))

# Count how many types have fixed bay across all solutions
determined_count = 0
for t in range(6):
    possible_bays = set(m[t] for m in models)
    if len(possible_bays) == 1:
        determined_count += 1

print(determined_count)