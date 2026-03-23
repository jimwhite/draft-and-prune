from z3 import *

# Member indices: 0-guitarist, 1-keyboard player, 2-saxophonist, 3-trumpeter, 4-violinist
# (percussionist is index 5 but not in answer choices)
members = ["guitarist", "keyboard player", "percussionist", "saxophonist", "trumpeter", "violinist"]
pos = [Int(f"pos_{i}") for i in range(6)]

# Base solver
solver = Solver()

# Domain constraints: positions 1-6, all distinct
for i in range(6):
    solver.add(pos[i] >= 1, pos[i] <= 6)
solver.add(Distinct(*pos))

# Guitarist constraint: does not perform the fourth solo
solver.add(pos[0] != 4)

# Percussionist < keyboard player
solver.add(pos[2] < pos[1])

# Violinist < keyboard player < guitarist
solver.add(pos[5] < pos[1])
solver.add(pos[1] < pos[0])

# Saxophonist performs after exactly one of percussionist or trumpeter (XOR)
solver.add((If(pos[2] < pos[3], 1, 0) + If(pos[3] < pos[2], 1, 0)) == 1)

# Answer choices indices: guitarist=0, keyboard player=1, saxophonist=2, trumpeter=3, violinist=4
answer_choices = [0, 1, 2, 3, 4]

# Check each answer choice
answer_index_list = []
for idx in answer_choices:
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert this member performs the third solo
    s_chk.add(pos[idx] == 3)
    
    # If UNSAT, this member cannot be third
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)