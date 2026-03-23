from z3 import *

# Cargo type indices: 0-fuel, 1-grain, 2-livestock, 3-machinery, 4-produce, 5-textiles
(FUEL, GRAIN, LIVESTOCK, MACHINERY, PRODUCE, TEXTILES) = range(6)

# Position variables: pos[type] = bay number (1-6)
pos = {t: Int(f"pos_{t}") for t in [FUEL, GRAIN, LIVESTOCK, MACHINERY, PRODUCE, TEXTILES]}

# Base solver
solver = Solver()

# Domain constraints: positions 1-6
for t in pos:
    solver.add(pos[t] >= 1, pos[t] <= 6)

# Distinctness constraint: each bay has exactly one cargo type
solver.add(Distinct(*pos.values()))

# Ordering constraints
solver.add(pos[GRAIN] > pos[LIVESTOCK])
solver.add(pos[LIVESTOCK] > pos[TEXTILES])
solver.add(pos[PRODUCE] > pos[FUEL])

# Textiles and produce are adjacent
solver.add(Or(pos[TEXTILES] == pos[PRODUCE] + 1, pos[TEXTILES] == pos[PRODUCE] - 1))

# Conditional constraint: exactly one bay between machinery and grain
solver.add(Or(pos[MACHINERY] == pos[GRAIN] + 2, pos[MACHINERY] == pos[GRAIN] - 2))

# Collect all satisfying assignments
models = []
while solver.check() == sat:
    model = solver.model()
    models.append(model)
    
    # Add constraint to exclude current model
    solver.add(Or(*[pos[t] != model[pos[t]] for t in pos]))

# For each bay position (1-6), check if cargo type is fixed across all models
fixed_count = 0
for bay in range(1, 7):
    cargo_types_at_bay = set()
    for model in models:
        # Find which cargo type is at this bay
        for t in pos:
            if model[pos[t]].as_long() == bay:
                cargo_types_at_bay.add(t)
                break
    if len(cargo_types_at_bay) == 1:
        fixed_count += 1

print(fixed_count)