from z3 import *

# Accomplice indices: P=Peters, Q=Quinn, R=Rovero, S=Stanton, T=Tao, V=Villas, W=White
accomplices = ["Peters", "Quinn", "Rovero", "Stanton", "Tao", "Villas", "White"]
pos = {a: Int(f"pos_{a}") for a in accomplices}

# Base solver with conditional assumption
solver = Solver()

# Domain constraints: positions 1-7, all distinct
for a in accomplices:
    solver.add(pos[a] >= 1, pos[a] <= 7)
solver.add(Distinct(*[pos[a] for a in accomplices]))

# Fixed constraint: Peters is fourth
solver.add(pos["Peters"] == 4)

# Relative ordering constraints:
# Quinn before Rovero
solver.add(pos["Quinn"] < pos["Rovero"])
# Villas immediately before White
solver.add(pos["White"] == pos["Villas"] + 1)
# Stanton not adjacent to Tao
solver.add(Abs(pos["Stanton"] - pos["Tao"]) != 1)

# Conditional assumption: Quinn immediately before Rovero
solver.add(pos["Rovero"] == pos["Quinn"] + 1)

# Answer choices: first=1, second=2, third=3, fifth=5, seventh=7
answer_choices = [1, 2, 3, 5, 7]

# Check each answer choice
impossible_positions = []
for candidate in answer_choices:
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add assumption that Stanton is at candidate position
    s_chk.add(pos["Stanton"] == candidate)
    
    # If UNSAT, Stanton cannot be at this position
    if s_chk.check() == unsat:
        impossible_positions.append(candidate)

print(impossible_positions)