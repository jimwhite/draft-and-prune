from z3 import *

# Role indices: 0=guitarist, 1=keyboard player, 2=percussionist, 3=saxophonist, 4=trumpeter, 5=violinist
roles = ["guitarist", "keyboard player", "percussionist", "saxophonist", "trumpeter", "violinist"]
pos = [Int(f"pos_{i}") for i in range(6)]

solver = Solver()

# Domain constraints: positions 1-6
for i in range(6):
    solver.add(pos[i] >= 1, pos[i] <= 6)

# All positions distinct
solver.add(Distinct(*pos))

# Guitarist does not perform the fourth solo
solver.add(pos[0] != 4)

# Percussionist before keyboard player
solver.add(pos[2] < pos[1])

# Violinist before keyboard player, and keyboard player before guitarist
solver.add(pos[5] < pos[1])
solver.add(pos[1] < pos[0])

# Saxophonist after exactly one of (percussionist, trumpeter)
A = pos[2] < pos[3]  # percussionist before saxophonist
B = pos[4] < pos[3]  # trumpeter before saxophonist
solver.add(Or(And(A, Not(B)), And(Not(A), B)))

# Answer choices: indices 0=guitarist, 1=keyboard player, 3=saxophonist, 4=trumpeter, 5=violinist
answer_choices = [0, 1, 3, 4, 5]

answer_index_list = []
for idx in answer_choices:
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert this role is third
    s_chk.add(pos[idx] == 3)
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)