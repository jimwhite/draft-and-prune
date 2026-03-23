from z3 import *

# Recruit indices
(PETERS, QUINN, ROVERO, STANTON, TAO, VILLAS, WHITE) = range(7)

# Position variables: pos[recruit] = recruitment position (1-7)
pos = {name: Int(f"pos_{name}") for name in ["Peters", "Quinn", "Rovero", "Stanton", "Tao", "Villas", "White"]}

# Base solver
solver = Solver()

# Domain constraints: positions 1-7 and all distinct
for name in pos:
    solver.add(pos[name] >= 1, pos[name] <= 7)
solver.add(Distinct(*pos.values()))

# Fixed constraint: Peters is fourth
solver.add(pos["Peters"] == 4)

# Villas immediately before White: pos[Villas] + 1 == pos[White]
solver.add(pos["Villas"] + 1 == pos["White"])

# Quinn immediately before Rovero (conditional constraint)
solver.add(pos["Quinn"] + 1 == pos["Rovero"])

# Stanton not immediately before or after Tao: |pos[Stanton] - pos[Tao]| != 1
solver.add(Not(pos["Stanton"] == pos["Tao"] - 1))
solver.add(Not(pos["Stanton"] == pos["Tao"] + 1))

# Answer choices positions (as indices for the list)
answer_positions = ["first", "second", "third", "fifth", "seventh"]
position_values = [1, 2, 3, 5, 7]

# Check each position for Stanton
answer_index_list = []
for idx, (label, pos_val) in enumerate(zip(answer_positions, position_values)):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraint that Stanton is at this position
    s_chk.add(pos["Stanton"] == pos_val)
    
    # Check if this is possible under the conditional (Quinn immediately before Rovero)
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)