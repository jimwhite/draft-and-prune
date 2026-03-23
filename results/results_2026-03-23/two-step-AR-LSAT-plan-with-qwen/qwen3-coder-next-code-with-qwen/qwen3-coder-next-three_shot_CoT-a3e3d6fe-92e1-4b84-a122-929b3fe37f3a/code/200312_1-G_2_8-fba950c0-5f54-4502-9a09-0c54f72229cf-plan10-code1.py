from z3 import *

# Cargo type indices: 0-fuel, 1-grain, 2-livestock, 3-machinery, 4-produce, 5-textiles
(FUEL, GRAIN, LIVESTOCK, MACHINERY, PRODUCE, TEXTILES) = range(6)

# Position variables: pos[type] = bay number (1-6)
pos = [Int(f"pos_{i}") for i in range(6)]

# Base solver
solver = Solver()

# Domain constraints: positions are distinct integers in [1,6]
solver.add(Distinct(pos))
for i in range(6):
    solver.add(pos[i] >= 1, pos[i] <= 6)

# Ordering constraints
solver.add(pos[GRAIN] > pos[LIVESTOCK])
solver.add(pos[LIVESTOCK] > pos[TEXTILES])
solver.add(pos[PRODUCE] > pos[FUEL])

# Adjacency constraint: textiles is next to produce
solver.add(Or(pos[PRODUCE] == pos[TEXTILES] + 1, pos[TEXTILES] == pos[PRODUCE] + 1))

# Conditional constraint: exactly one bay between machinery and grain
solver.add(Or(pos[GRAIN] == pos[MACHINERY] + 2, pos[MACHINERY] == pos[GRAIN] + 2))

# Collect all satisfying models
models = []
while solver.check() == sat:
    m = solver.model()
    models.append(m)
    # Add constraint to exclude current model
    solver.add(Or(*[pos[i] != m[pos[i]] for i in range(6)]))

# For each cargo type, collect all possible positions across models
positions_per_type = [[] for _ in range(6)]
for m in models:
    for i in range(6):
        positions_per_type[i].append(m[pos[i]].as_long())

# Count how many cargo types have exactly one possible position
determined_count = sum(1 for positions in positions_per_type if len(set(positions)) == 1)

# Map count to answer string
answer_map = {2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six'}
print(answer_map[determined_count])