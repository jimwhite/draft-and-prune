from z3 import *

# Accomplice names
accomplices = ["Peters", "Quinn", "Rovero", "Stanton", "Tao", "Villas", "White"]

# Position variables
pos = {name: Int(f"pos_{name}") for name in accomplices}

# Base solver
solver = Solver()

# Domain constraints: positions 1 to 7
for name in accomplices:
    solver.add(pos[name] >= 1, pos[name] <= 7)

# All positions distinct
solver.add(Distinct(*[pos[name] for name in accomplices]))

# Fixed position: Peters is fourth
solver.add(pos["Peters"] == 4)

# Villas immediately before White: pos[Villas] + 1 == pos[White]
solver.add(pos["Villas"] + 1 == pos["White"])

# Quinn recruited earlier than Rovero
solver.add(pos["Quinn"] < pos["Rovero"])

# Stanton not adjacent to Tao
solver.add(Abs(pos["Stanton"] - pos["Tao"]) != 1)

# Choices to validate
choices = [
    ["Quinn", "Tao", "Stanton", "Peters", "Villas", "White", "Rovero"],
    ["Quinn", "White", "Rovero", "Peters", "Stanton", "Villas", "Tao"],
    ["Villas", "White", "Quinn", "Stanton", "Peters", "Tao", "Rovero"],
    ["Villas", "White", "Stanton", "Peters", "Quinn", "Tao", "Rovero"],
    ["Villas", "White", "Stanton", "Peters", "Rovero", "Tao", "Quinn"]
]

valid_indices = []

for idx, choice in enumerate(choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add position constraints implied by the choice
    for i, name in enumerate(choice):
        s_chk.add(pos[name] == i + 1)
    
    if s_chk.check() == sat:
        valid_indices.append(idx)

print(valid_indices)