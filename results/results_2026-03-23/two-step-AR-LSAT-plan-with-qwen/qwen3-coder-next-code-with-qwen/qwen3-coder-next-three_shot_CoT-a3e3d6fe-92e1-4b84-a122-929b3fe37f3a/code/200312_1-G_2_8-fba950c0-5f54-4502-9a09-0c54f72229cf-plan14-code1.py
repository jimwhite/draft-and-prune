from z3 import *

# Cargo type indices: 0-fuel, 1-grain, 2-livestock, 3-machinery, 4-produce, 5-textiles
cargo_types = ["fuel", "grain", "livestock", "machinery", "produce", "textiles"]
pos = {t: Int(f"pos_{t}") for t in cargo_types}

# Base solver
solver = Solver()

# Domain constraints: positions 1-6, all distinct
for t in cargo_types:
    solver.add(pos[t] >= 1, pos[t] <= 6)
solver.add(Distinct(*[pos[t] for t in cargo_types]))

# Relative ordering constraints
solver.add(pos["grain"] > pos["livestock"])
solver.add(pos["livestock"] > pos["textiles"])
solver.add(pos["produce"] > pos["fuel"])

# Textiles and produce are adjacent
solver.add(Or(pos["textiles"] == pos["produce"] + 1, pos["textiles"] == pos["produce"] - 1))

# Additional constraint: exactly one bay between machinery and grain
solver.add(Or(pos["machinery"] == pos["grain"] + 2, pos["machinery"] == pos["grain"] - 2))

# Collect all satisfying assignments
models = []
while solver.check() == sat:
    model = solver.model()
    models.append(model)
    
    # Block current assignment
    block = []
    for t in cargo_types:
        block.append(pos[t] != model.eval(pos[t]).as_long())
    solver.add(Or(block))

# For each cargo type, check if its position is uniquely determined across all models
determined_count = 0
for t in cargo_types:
    positions = set()
    for model in models:
        pos_val = model.eval(pos[t]).as_long()
        positions.add(pos_val)
    if len(positions) == 1:
        determined_count += 1

print(determined_count)