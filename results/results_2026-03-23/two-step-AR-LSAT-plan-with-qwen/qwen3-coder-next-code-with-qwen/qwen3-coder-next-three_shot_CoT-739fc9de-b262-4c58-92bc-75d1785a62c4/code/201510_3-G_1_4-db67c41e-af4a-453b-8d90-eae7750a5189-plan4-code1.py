from z3 import *

# Accomplice position variables: pos[name] = recruitment position (1-7)
names = ["Peters", "Quinn", "Rovero", "Stanton", "Tao", "Villas", "White"]
pos = {name: Int(f"pos_{name}") for name in names}

# Base solver
solver = Solver()

# Domain constraints: positions 1-7, all distinct
for name in names:
    solver.add(pos[name] >= 1, pos[name] <= 7)
solver.add(Distinct(*[pos[name] for name in names]))

# Fixed constraint: Peters is recruited fourth
solver.add(pos["Peters"] == 4)

# Villas immediately before White: pos_Villas + 1 == pos_White
solver.add(pos["Villas"] + 1 == pos["White"])

# Quinn earlier than Rovero: pos_Quinn < pos_Rovero
solver.add(pos["Quinn"] < pos["Rovero"])

# Stanton not immediately before or after Tao: |pos_Stanton - pos_Tao| != 1
solver.add(Abs(pos["Stanton"] - pos["Tao"]) != 1)

# Conditional constraint: Quinn immediately before Rovero
solver.add(pos["Quinn"] + 1 == pos["Rovero"])

# Answer choices: ['first', 'second', 'third', 'fifth', 'seventh']
# Map to positions: first=1, second=2, third=3, fifth=5, seventh=7
answer_positions = [1, 2, 3, 5, 7]

# Check each position for Stanton
answer_index_list = []
for idx, target_pos in enumerate(answer_positions):
    s_chk = Solver()
    # Add all base constraints + conditional constraint
    for a in solver.assertions():
        s_chk.add(a)
    
    # Add constraint that Stanton is at target position
    s_chk.add(pos["Stanton"] == target_pos)
    
    # If UNSAT, Stanton cannot be in this position
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)