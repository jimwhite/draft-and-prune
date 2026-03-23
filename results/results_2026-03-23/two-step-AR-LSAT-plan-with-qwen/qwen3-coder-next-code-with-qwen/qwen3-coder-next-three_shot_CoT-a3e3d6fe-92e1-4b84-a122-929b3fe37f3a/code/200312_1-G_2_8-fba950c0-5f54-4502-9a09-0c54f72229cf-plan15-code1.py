from z3 import *

# Cargo types: fuel, grain, livestock, machinery, produce, textiles
cargo_types = ["fuel", "grain", "livestock", "machinery", "produce", "textiles"]
num_cargos = len(cargo_types)

# Position variables: pos[type] = bay number (1-6)
pos = {c: Int(f"pos_{c}") for c in cargo_types}

# Base solver
solver = Solver()

# Domain constraints: each position between 1 and 6, all distinct
for c in cargo_types:
    solver.add(pos[c] >= 1, pos[c] <= 6)
solver.add(Distinct(*[pos[c] for c in cargo_types]))

# Ordering constraints
solver.add(pos["grain"] > pos["livestock"])
solver.add(pos["livestock"] > pos["textiles"])
solver.add(pos["produce"] > pos["fuel"])
# Textiles and produce are adjacent
solver.add(Or(pos["produce"] == pos["textiles"] + 1, pos["produce"] == pos["textiles"] - 1))

# Conditional constraint: exactly one bay between machinery and grain
solver.add(Or(pos["grain"] == pos["machinery"] + 2, pos["grain"] == pos["machinery"] - 2))

# For each bay (1-6) and cargo type, check if it's possible
possible = {}
for b in range(1, 7):
    possible[b] = set()
    for c in cargo_types:
        s_chk = Solver()
        s_chk.add(solver.assertions())
        s_chk.add(pos[c] == b)
        if s_chk.check() == sat:
            possible[b].add(c)

# Count bays where exactly one cargo type is possible
determined_count = sum(1 for b in range(1, 7) if len(possible[b]) == 1)

# Map to answer choices
answers = ['two', 'three', 'four', 'five', 'six']
print(answers[determined_count - 2] if determined_count >= 2 and determined_count <= 6 else str(determined_count))