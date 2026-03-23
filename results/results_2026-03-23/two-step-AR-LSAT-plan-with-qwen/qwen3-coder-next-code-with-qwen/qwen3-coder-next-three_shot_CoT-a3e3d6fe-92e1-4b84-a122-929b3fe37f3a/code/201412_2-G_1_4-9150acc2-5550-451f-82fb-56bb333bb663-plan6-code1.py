from z3 import *

# Role indices: 0=guitarist, 1=keyboard player, 2=percussionist, 3=saxophonist, 4=trumpeter, 5=violinist
roles = ["guitarist", "keyboard player", "percussionist", "saxophonist", "trumpeter", "violinist"]
pos = [Int(f"pos_{i}") for i in range(6)]

# Base solver
solver = Solver()

# Domain constraints: each position is between 1 and 6, all distinct
for i in range(6):
    solver.add(pos[i] >= 1, pos[i] <= 6)
solver.add(Distinct(*pos))

# Guitarist constraint: does not perform the fourth solo
solver.add(pos[0] != 4)

# Percussionist performs before keyboard player: pos[2] < pos[1]
solver.add(pos[2] < pos[1])

# Violinist < keyboard player < guitarist: pos[5] < pos[1] and pos[1] < pos[0]
solver.add(pos[5] < pos[1])
solver.add(pos[1] < pos[0])

# Saxophonist performs after exactly one of percussionist or trumpeter (XOR)
sax_after_per = pos[3] > pos[2]
sax_after_trump = pos[3] > pos[4]
solver.add(Xor(sax_after_per, sax_after_trump))

# Answer choices: indices for ['guitarist', 'keyboard player', 'saxophonist', 'trumpeter', 'violinist']
answer_roles = [0, 1, 3, 4, 5]

# Check each answer choice
answer_index_list = []
for idx in answer_roles:
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraint that this role is third
    s_chk.add(pos[idx] == 3)
    
    # If UNSAT, this role cannot be third
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)