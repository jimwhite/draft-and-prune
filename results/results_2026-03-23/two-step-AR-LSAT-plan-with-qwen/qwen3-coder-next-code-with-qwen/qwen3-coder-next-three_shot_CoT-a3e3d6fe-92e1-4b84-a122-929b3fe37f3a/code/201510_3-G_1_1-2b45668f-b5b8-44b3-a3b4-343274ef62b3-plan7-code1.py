from z3 import *

# Accomplice names and their position variables
names = ["Peters", "Quinn", "Rovero", "Stanton", "Tao", "Villas", "White"]
positions = {name: Int(f"{name.lower()}_pos") for name in names}

# Base solver
solver = Solver()

# Domain constraints: positions are 0-6 (first to seventh)
for name in names:
    solver.add(positions[name] >= 0, positions[name] <= 6)

# All-different constraint
solver.add(Distinct(*[positions[name] for name in names]))

# Peters is fourth → position 3
solver.add(positions["Peters"] == 3)

# Villas immediately before White → villas_pos + 1 == white_pos
solver.add(positions["Villas"] + 1 == positions["White"])

# Quinn earlier than Rovero → quinn_pos < rovero_pos
solver.add(positions["Quinn"] < positions["Rovero"])

# Stanton neither immediately before nor after Tao → |stanton_pos - tao_pos| != 1
solver.add(Abs(positions["Stanton"] - positions["Tao"]) != 1)

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
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Hardcode positions based on the choice (0-indexed)
    for i, name in enumerate(choice):
        s_chk.add(positions[name] == i)
    
    if s_chk.check() == sat:
        valid_indices.append(idx)

# Since only one choice should be correct, output the corresponding string
if len(valid_indices) == 1:
    print(answer_choices[valid_indices[0]])