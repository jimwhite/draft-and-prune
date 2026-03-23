from z3 import *

# Accomplice names and fixed index for Peters (4th position)
accomplices = ["Peters", "Quinn", "Rovero", "Stanton", "Tao", "Villas", "White"]
peters_idx = 0  # Peters is fixed at position 4 (index 3 in 0-based, but we use 1-based positions)

# Create position variables
pos = {name: Int(f"pos_{name}") for name in accomplices}

# Base solver
solver = Solver()

# Domain constraints: positions 1-7, all distinct
for name in accomplices:
    solver.add(pos[name] >= 1, pos[name] <= 7)
solver.add(Distinct(*[pos[name] for name in accomplices]))

# Fixed constraint: Peters is 4th
solver.add(pos["Peters"] == 4)

# Ordering constraint: Quinn before Rovero
solver.add(pos["Quinn"] < pos["Rovero"])

# Adjacency constraint: Villas immediately before White
solver.add(pos["White"] == pos["Villas"] + 1)

# Non-adjacency constraint: Stanton not immediately before or after Tao
solver.add(Abs(pos["Stanton"] - pos["Tao"]) != 1)

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
    
    # Assert positions match the order (1st -> position 1, etc.)
    for i, name in enumerate(order):
        s_chk.add(pos[name] == i + 1)
    
    if s_chk.check() == sat:
        valid_indices.append(idx)

# Output the first valid choice (as per question format)
if valid_indices:
    print(answer_choices[valid_indices[0]])
else:
    print([])