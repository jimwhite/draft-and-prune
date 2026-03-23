from z3 import *

# Recruit indices
(PETERS, QUINN, ROVERO, STANTON, TAO, VILLAS, WHITE) = range(7)

# Position variables (1 to 7)
pos = {name: Int(f"pos_{name}") for name in ["Peters", "Quinn", "Rovero", "Stanton", "Tao", "Villas", "White"]}

# Base solver
solver = Solver()

# Domain constraints: positions 1-7, all distinct
for name in pos:
    solver.add(pos[name] >= 1, pos[name] <= 7)
solver.add(Distinct(*pos.values()))

# Fixed constraint: Peters is fourth
solver.add(pos["Peters"] == 4)

# Villas immediately before White
solver.add(pos["Villas"] + 1 == pos["White"])

# Quinn earlier than Rovero
solver.add(pos["Quinn"] < pos["Rovero"])

# Stanton and Tao not adjacent
solver.add(Abs(pos["Stanton"] - pos["Tao"]) != 1)

# Additional condition: Quinn immediately before Rovero
solver.add(pos["Quinn"] + 1 == pos["Rovero"])

# Answer options mapped to positions
answer_options = [
    ("first", 1),
    ("second", 2),
    ("third", 3),
    ("fifth", 5),
    ("seventh", 7)
]

# Check each option
impossible_positions = []
for label, position in answer_options:
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(pos["Stanton"] == position)
    
    if s_chk.check() == unsat:
        impossible_positions.append(label)

print(impossible_positions)