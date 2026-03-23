from z3 import *

# Cargo type indices: fuel=0, grain=1, livestock=2, machinery=3, produce=4, textiles=5
cargo_types = ["fuel", "grain", "livestock", "machinery", "produce", "textiles"]

# Position variables: pos[type] = bay number (1-6)
pos = {t: Int(f"pos_{t}") for t in cargo_types}

# Base solver
solver = Solver()

# Domain constraints: each position is between 1 and 6, all distinct
for t in cargo_types:
    solver.add(pos[t] >= 1, pos[t] <= 6)
solver.add(Distinct(*[pos[t] for t in cargo_types]))

# Given inequality constraints
solver.add(pos["grain"] > pos["livestock"])
solver.add(pos["livestock"] > pos["textiles"])
solver.add(pos["produce"] > pos["fuel"])

# Textiles and produce are adjacent
solver.add(Or(pos["textiles"] == pos["produce"] + 1, pos["textiles"] == pos["produce"] - 1))

# Additional constraint for the conditional scenario: produce is next to livestock
solver.add(Or(pos["produce"] == pos["livestock"] + 1, pos["produce"] == pos["livestock"] - 1))

# Answer choices
answer_choices = [
    ("fuel", 2),      # Bay 2 is holding fuel.
    ("produce", 4),   # Bay 4 is holding produce.
    ("textiles", 4),  # Bay 4 is holding textiles.
    ("grain", 5),     # Bay 5 is holding grain.
    ("machinery", 5)  # Bay 5 is holding machinery.
]

# Check each answer choice
answer_index_list = []
for idx, (cargo_type, bay_num) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraint for the specific choice
    s_chk.add(pos[cargo_type] == bay_num)
    
    # If UNSAT, this choice cannot be true (EXCEPT answer)
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)