from z3 import *

# Cargo types: fuel (0), grain (1), livestock (2), machinery (3), produce (4), textiles (5)
cargo_types = ["fuel", "grain", "livestock", "machinery", "produce", "textiles"]

# Position variables: pos[cargo_type] = position (1-6)
pos = {c: Int(f"pos_{c}") for c in cargo_types}

# Base solver
solver = Solver()

# Domain constraints: each position between 1 and 6
for c in cargo_types:
    solver.add(pos[c] >= 1, pos[c] <= 6)

# Uniqueness constraint: all positions distinct
solver.add(Distinct(*[pos[c] for c in cargo_types]))

# Base ordering constraints
solver.add(pos["grain"] > pos["livestock"])
solver.add(pos["livestock"] > pos["textiles"])
solver.add(pos["produce"] > pos["fuel"])
# Textiles is next to produce
solver.add(Or(pos["textiles"] == pos["produce"] + 1, pos["textiles"] == pos["produce"] - 1))

# Conditional constraint (the "if" premise): produce is next to livestock
solver.add(Or(pos["produce"] == pos["livestock"] + 1, pos["produce"] == pos["livestock"] - 1))

# Answer choices (negated for EXCEPT logic)
answer_choices = [
    ("fuel", 2),      # A. Bay 2 is holding fuel
    ("produce", 4),   # B. Bay 4 is holding produce
    ("textiles", 4),  # C. Bay 4 is holding textiles
    ("grain", 5),     # D. Bay 5 is holding grain
    ("machinery", 5)  # E. Bay 5 is holding machinery
]

# Check each answer choice using proof by contradiction
impossible_indices = []
for idx, (cargo, bay) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert the specific position constraint for this choice
    s_chk.add(pos[cargo] == bay)
    
    # If UNSAT, this choice cannot be true under the premise (EXCEPT answer)
    if s_chk.check() == unsat:
        impossible_indices.append(idx)

print(impossible_indices)