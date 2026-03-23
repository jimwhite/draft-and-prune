from z3 import *

# Cargo types indices: 0-fuel, 1-grain, 2-livestock, 3-machinery, 4-produce, 5-textiles
(FUEL, GRAIN, LIVESTOCK, MACHINERY, PRODUCE, TEXTILES) = range(6)

# Position variables: pos[c] is the bay number (1-6) for cargo type c
pos = {c: Int(f"pos_{c}") for c in range(6)}

# Base solver
solver = Solver()

# Domain constraints: positions 1-6, all distinct
for c in range(6):
    solver.add(pos[c] >= 1, pos[c] <= 6)
solver.add(Distinct(*[pos[c] for c in range(6)]))

# Order constraints
solver.add(pos[GRAIN] > pos[LIVESTOCK])
solver.add(pos[LIVESTOCK] > pos[TEXTILES])
solver.add(pos[PRODUCE] > pos[FUEL])

# Textiles adjacent to produce
solver.add(Or(pos[PRODUCE] == pos[TEXTILES] + 1, pos[TEXTILES] == pos[PRODUCE] + 1))

# Conditional constraint: exactly one bay between machinery and grain
solver.add(Or(pos[GRAIN] == pos[MACHINERY] + 2, pos[MACHINERY] == pos[GRAIN] + 2))

# Collect all models
models = []
while solver.check() == sat:
    m = solver.model()
    models.append(m)
    # Add constraint to exclude current model
    solver.add(Or(*[pos[c] != m.eval(pos[c]).as_long() for c in range(6)]))

# For each bay position (1-6), determine if cargo type is fixed across all models
fixed_bays = 0
for bay in range(1, 7):
    cargo_type_set = set()
    for m in models:
        # Find which cargo type is at position 'bay'
        for c in range(6):
            if m.eval(pos[c]).as_long() == bay:
                cargo_type_set.add(c)
                break
    if len(cargo_type_set) == 1:
        fixed_bays += 1

# Map count to answer string
answer_map = {2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six'}
print(answer_map[fixed_bays])