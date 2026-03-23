from z3 import *

# Cargo types: fuel=0, grain=1, livestock=2, machinery=3, produce=4, textiles=5
cargo_types = ["fuel", "grain", "livestock", "machinery", "produce", "textiles"]

# Position variables: pos[c] = bay number (1-6) for cargo type c
pos = {c: Int(f"pos_{c}") for c in cargo_types}

# Base solver
solver = Solver()

# Domain constraints: each position between 1 and 6, all distinct
for c in cargo_types:
    solver.add(pos[c] >= 1, pos[c] <= 6)
solver.add(Distinct(*[pos[c] for c in cargo_types]))

# Given ordering constraints
solver.add(pos["grain"] > pos["livestock"])
solver.add(pos["livestock"] > pos["textiles"])
solver.add(pos["produce"] > pos["fuel"])
# Textiles adjacent to produce
solver.add(Or(pos["produce"] == pos["textiles"] + 1, pos["produce"] == pos["textiles"] - 1))

# Conditional constraint (the "if" premise): produce is next to livestock
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
for idx, (cargo, bay) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert the choice's condition
    s_chk.add(pos[cargo] == bay)
    
    # If UNSAT, this choice cannot be true under the premise (EXCEPT answer)
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

# Print the corresponding choice string
choices_str = [
    'Bay 2 is holding fuel.',
    'Bay 4 is holding produce.',
    'Bay 4 is holding textiles.',
    'Bay 5 is holding grain.',
    'Bay 5 is holding machinery.'
]

print(choices_str[answer_index_list[0]])