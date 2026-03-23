from z3 import *

# Accomplice indices (names)
acc = ["Peters", "Quinn", "Rovero", "Stanton", "Tao", "Villas", "White"]
pos = {name: Int(f"pos_{name}") for name in acc}

# Base solver
solver = Solver()

# Domain constraints: positions 1 to 7
for name in acc:
    solver.add(pos[name] >= 1, pos[name] <= 7)

# Distinctness constraint
solver.add(Distinct(*[pos[name] for name in acc]))

# Peters fixed: 4th position
solver.add(pos["Peters"] == 4)

# Villas immediately before White: pos_Villas + 1 == pos_White
solver.add(pos["Villas"] + 1 == pos["White"])

# Quinn before Rovero
solver.add(pos["Quinn"] < pos["Rovero"])

# Stanton and Tao not adjacent: |pos_Stanton - pos_Tao| != 1
solver.add(Or(pos["Stanton"] + 1 < pos["Tao"], pos["Tao"] + 1 < pos["Stanton"]))

# Answer choices
choices = [
    ["Quinn", "Tao", "Stanton", "Peters", "Villas", "White", "Rovero"],
    ["Quinn", "White", "Rovero", "Peters", "Stanton", "Villas", "Tao"],
    ["Villas", "White", "Quinn", "Stanton", "Peters", "Tao", "Rovero"],
    ["Villas", "White", "Stanton", "Peters", "Quinn", "Tao", "Rovero"],
    ["Villas", "White", "Stanton", "Peters", "Rovero", "Tao", "Quinn"]
]

# Check each choice
valid_indices = []
for idx, choice in enumerate(choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Enforce the order: position i+1 must be assigned to choice[i]
    for i, name in enumerate(choice):
        s_chk.add(pos[name] == i + 1)
    
    if s_chk.check() == sat:
        valid_indices.append(idx)

# Output the first valid choice (as per question format)
if valid_indices:
    print(choices[valid_indices[0]])
else:
    print([])