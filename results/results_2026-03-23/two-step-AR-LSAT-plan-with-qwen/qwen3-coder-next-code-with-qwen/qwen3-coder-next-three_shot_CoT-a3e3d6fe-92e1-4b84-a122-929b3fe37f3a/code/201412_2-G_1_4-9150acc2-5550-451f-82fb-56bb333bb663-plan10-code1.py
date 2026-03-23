from z3 import *

# Role indices: 0-guitarist, 1-keyboard player, 2-percussionist, 
#               3-saxophonist, 4-trumpeter, 5-violinist
roles = ["guitarist", "keyboard player", "percussionist", "saxophonist", "trumpeter", "violinist"]
pos = [Int(f"pos_{i}") for i in range(6)]

# Base solver
solver = Solver()

# Domain constraints: positions 1-6, all distinct
for i in range(6):
    solver.add(pos[i] >= 1, pos[i] <= 6)
solver.add(Distinct(pos))

# Guitarist constraint: does not perform the fourth solo
solver.add(pos[0] != 4)

# Percussionist before keyboard player
solver.add(pos[2] < pos[1])

# Violinist before keyboard player, keyboard player before guitarist
solver.add(pos[5] < pos[1])
solver.add(pos[1] < pos[0])

# Saxophonist performs after exactly one of (percussionist, trumpeter)
# XOR: (pos[3] > pos[2]) + (pos[3] > pos[4]) == 1
solver.add((If(pos[3] > pos[2], 1, 0) + If(pos[3] > pos[4], 1, 0)) == 1)

# Answer choices indices: ['guitarist', 'keyboard player', 'saxophonist', 'trumpeter', 'violinist']
# -> indices [0, 1, 3, 4, 5]
answer_choices = [0, 1, 3, 4, 5]

# Check each answer choice
answer_index_list = []
for idx in answer_choices:
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraint that this role performs third
    s_chk.add(pos[idx] == 3)
    
    # If UNSAT, this role CANNOT perform third
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)