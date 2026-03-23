from z3 import *

# Role indices: 0-guitarist, 1-keyboard player, 2-percussionist, 3-saxophonist, 4-trumpeter, 5-violinist
roles = ["guitarist", "keyboard player", "percussionist", "saxophonist", "trumpeter", "violinist"]
pos = [Int(f"pos_{i}") for i in range(6)]

# Base solver
solver = Solver()

# Domain constraints: positions 1-6
for i in range(6):
    solver.add(pos[i] >= 1, pos[i] <= 6)

# Distinctness constraint
solver.add(Distinct(pos))

# Guitarist does not perform 4th solo
solver.add(pos[0] != 4)

# Percussionist before keyboard player
solver.add(pos[2] < pos[1])

# Violinist before keyboard player, keyboard player before guitarist
solver.add(pos[5] < pos[1])
solver.add(pos[1] < pos[0])

# Saxophonist after exactly one of percussionist or trumpeter
solver.add((If(pos[3] > pos[2], 1, 0) + If(pos[3] > pos[4], 1, 0)) == 1)

# Answer choices indices: [guitarist=0, keyboard player=1, saxophonist=3, trumpeter=4, violinist=5]
answer_choices = [0, 1, 3, 4, 5]

# Check each answer choice
impossible_third_list = []
for idx in answer_choices:
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraint that this role is third
    s_chk.add(pos[idx] == 3)
    
    # If UNSAT, this role cannot be third
    if s_chk.check() == unsat:
        impossible_third_list.append(idx)

print(impossible_third_list)