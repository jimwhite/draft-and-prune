from z3 import *

# Accomplice indices: Peters=0, Quinn=1, Rovero=2, Stanton=3, Tao=4, Villas=5, White=6
accomplices = ["Peters", "Quinn", "Rovero", "Stanton", "Tao", "Villas", "White"]
pos = {p: Int(f"pos_{p}") for p in accomplices}

# Base solver
solver = Solver()

# Domain constraints: positions 1-7, all distinct
for p in accomplices:
    solver.add(pos[p] >= 1, pos[p] <= 7)
solver.add(Distinct(*[pos[p] for p in accomplices]))

# Fixed constraint: Peters is recruited fourth
solver.add(pos["Peters"] == 4)

# Villas-White adjacency constraint: Villas immediately before White
solver.add(pos["Villas"] + 1 == pos["White"])

# Quinn-before-Rovero constraint
solver.add(pos["Quinn"] < pos["Rovero"])

# Stanton-Tao non-adjacency constraint: |pos_Stanton - pos_Tao| != 1
solver.add(Or(pos["Stanton"] + 1 < pos["Tao"], pos["Tao"] + 1 < pos["Stanton"]))

# Answer choices
answer_choices = [
    ["Quinn", "Tao", "Stanton", "Peters", "Villas", "White", "Rovero"],
    ["Quinn", "White", "Rovero", "Peters", "Stanton", "Villas", "Tao"],
    ["Villas", "White", "Quinn", "Stanton", "Peters", "Tao", "Rovero"],
    ["Villas", "White", "Stanton", "Peters", "Quinn", "Tao", "Rovero"],
    ["Villas", "White", "Stanton", "Peters", "Rovero", "Tao", "Quinn"]
]

# Check each answer choice
valid_indices = []
for idx, order in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add position constraints for this specific order
    for i, p in enumerate(order):
        s_chk.add(pos[p] == i + 1)
    
    if s_chk.check() == sat:
        valid_indices.append(idx)

# Output the first valid index (as per multiple-choice expectation)
print(valid_indices[0] if valid_indices else -1)