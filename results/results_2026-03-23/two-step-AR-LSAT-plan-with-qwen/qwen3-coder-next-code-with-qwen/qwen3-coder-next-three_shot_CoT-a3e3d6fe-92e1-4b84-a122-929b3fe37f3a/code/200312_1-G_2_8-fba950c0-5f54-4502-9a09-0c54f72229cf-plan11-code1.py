from z3 import *

# Cargo types: 0-fuel, 1-grain, 2-livestock, 3-machinery, 4-produce, 5-textiles
(FUEL, GRAIN, LIVESTOCK, MACHINERY, PRODUCE, TEXTILES) = range(6)

# bay[c] = position (1-6) where cargo type c is stored
bay = [Int(f"bay_{c}") for c in range(6)]

solver = Solver()

# Domain constraints: each bay position between 1 and 6
for c in range(6):
    solver.add(bay[c] >= 1, bay[c] <= 6)

# All bays distinct
solver.add(Distinct(bay))

# Ordering constraints
solver.add(bay[GRAIN] > bay[LIVESTOCK])
solver.add(bay[LIVESTOCK] > bay[TEXTILES])
solver.add(bay[PRODUCE] > bay[FUEL])

# Textiles and produce are adjacent
solver.add(Or(bay[TEXTILES] == bay[PRODUCE] + 1, bay[TEXTILES] == bay[PRODUCE] - 1))

# Exactly one bay between machinery and grain: |bay[MACHINERY] - bay[GRAIN]| == 2
solver.add(Or(bay[MACHINERY] == bay[GRAIN] + 2, bay[MACHINERY] == bay[GRAIN] - 2))

# Collect all possible assignments
models = []
while solver.check() == sat:
    m = solver.model()
    models.append(m)
    # Block current model
    block = [bay[c] != m[bay[c]] for c in range(6)]
    solver.add(Or(block))

# For each bay position p (1-6), collect which cargo types can be there
bay_to_cargos = {p: set() for p in range(1, 7)}
for m in models:
    for c in range(6):
        p = m[bay[c]].as_long()
        bay_to_cargos[p].add(c)

# Count how many bays have exactly one possible cargo type
determined_count = sum(1 for p in range(1, 7) if len(bay_to_cargos[p]) == 1)

# Map count to answer choice
answer_map = {2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six'}
print(answer_map[determined_count])