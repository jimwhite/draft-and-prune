from z3 import *

# Role indices: 0=guitarist, 1=keyboard player, 2=percussionist, 3=saxophonist, 4=trumpeter, 5=violinist
roles = ["guitarist", "keyboard player", "percussionist", "saxophonist", "trumpeter", "violinist"]
pos = [Int(f"pos_{i}") for i in range(6)]

# Base solver
solver = Solver()

# Domain constraints: positions 1-6, all distinct
for i in range(6):
    solver.add(pos[i] >= 1, pos[i] <= 6)
solver.add(Distinct(pos))

# Guitarist does not perform the fourth solo
solver.add(pos[0] != 4)

# Percussionist before keyboard player
solver.add(pos[2] < pos[1])

# Violinist before keyboard player, keyboard player before guitarist
solver.add(pos[5] < pos[1])
solver.add(pos[1] < pos[0])

# Saxophonist performs after exactly one of {percussionist, trumpeter}
s_after_p = pos[3] > pos[2]
s_after_t = pos[3] > pos[4]
solver.add(s_after_p != s_after_t)

# Answer choices (indices): 0=guitarist, 1=keyboard player, 3=saxophonist, 4=trumpeter, 5=violinist
answer_choices = [0, 1, 3, 4, 5]

# Check each answer choice
answer_index_list = []
for r in answer_choices:
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert role r is third
    s_chk.add(pos[r] == 3)
    
    if s_chk.check() == unsat:
        answer_index_list.append(r)

print(answer_index_list)