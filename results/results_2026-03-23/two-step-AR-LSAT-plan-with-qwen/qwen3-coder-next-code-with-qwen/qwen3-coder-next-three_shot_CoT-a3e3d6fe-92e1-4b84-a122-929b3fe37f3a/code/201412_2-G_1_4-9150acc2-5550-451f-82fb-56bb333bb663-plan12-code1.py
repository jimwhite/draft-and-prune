from z3 import *

# Role indices: 0=guitarist, 1=keyboard player, 2=percussionist, 3=saxophonist, 4=trumpeter, 5=violinist
roles = ["guitarist", "keyboard player", "percussionist", "saxophonist", "trumpeter", "violinist"]
pos = {r: Int(f"pos_{i}") for i, r in enumerate(roles)}

# Base solver
solver = Solver()

# Domain constraints: positions 1-6, all distinct
for i in range(6):
    solver.add(pos[roles[i]] >= 1, pos[roles[i]] <= 6)
solver.add(Distinct(*[pos[r] for r in roles]))

# Guitarist constraint: does not perform the fourth solo
solver.add(pos["guitarist"] != 4)

# Percussionist performs before keyboard player
solver.add(pos["percussionist"] < pos["keyboard player"])

# Violinist < keyboard player < guitarist
solver.add(pos["violinist"] < pos["keyboard player"])
solver.add(pos["keyboard player"] < pos["guitarist"])

# Saxophonist performs after either percussionist or trumpeter, but not both (XOR)
solver.add((pos["saxophonist"] > pos["percussionist"]) != (pos["saxophonist"] > pos["trumpeter"]))

# Answer choices: indices for ["guitarist", "keyboard player", "saxophonist", "trumpeter", "violinist"]
answer_choices = [0, 1, 3, 4, 5]
role_names = ["guitarist", "keyboard player", "percussionist", "saxophonist", "trumpeter", "violinist"]

# Check each answer choice
answer_index_list = []
for idx in answer_choices:
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraint that this role is third
    s_chk.add(pos[role_names[idx]] == 3)
    
    # If UNSAT, this role cannot be third
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)