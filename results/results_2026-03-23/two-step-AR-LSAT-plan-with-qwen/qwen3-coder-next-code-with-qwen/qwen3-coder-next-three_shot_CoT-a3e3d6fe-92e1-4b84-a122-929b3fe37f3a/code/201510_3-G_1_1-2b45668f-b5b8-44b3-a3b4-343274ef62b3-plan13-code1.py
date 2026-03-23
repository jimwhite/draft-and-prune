from z3 import *

# Accomplice names and their position variables
accomplices = ["Peters", "Quinn", "Rovero", "Stanton", "Tao", "Villas", "White"]
pos = {name: Int(f"pos_{name}") for name in accomplices}

# Base solver
solver = Solver()

# Domain constraints: positions 1-7, all distinct
for name in accomplices:
    solver.add(pos[name] >= 1, pos[name] <= 7)
solver.add(Distinct(*[pos[name] for name in accomplices]))

# Fixed constraint: Peters is recruited fourth
solver.add(pos["Peters"] == 4)

# Villas-White adjacency constraint: Villas immediately before White
solver.add(pos["White"] == pos["Villas"] + 1)

# Quinn-Rovero ordering constraint: Quinn earlier than Rovero
solver.add(pos["Quinn"] < pos["Rovero"])

# Stanton-Tao separation constraint: not adjacent
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
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert the order matches the candidate sequence
    for i, name in enumerate(choice):
        s_chk.add(pos[name] == i + 1)
    
    if s_chk.check() == sat:
        print(idx)
        break