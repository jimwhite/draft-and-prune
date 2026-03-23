from z3 import *

# Role indices: guitarist=0, keyboard player=1, percussionist=2, saxophonist=3, trumpeter=4, violinist=5
roles = ["guitarist", "keyboard player", "percussionist", "saxophonist", "trumpeter", "violinist"]
role_indices = {r: i for i, r in enumerate(roles)}

# Position variables
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

# Keyboard after violinist and before guitarist
solver.add(pos[5] < pos[1])
solver.add(pos[1] < pos[0])

# Saxophonist after exactly one of percussionist or trumpeter
after_per = pos[3] > pos[2]
after_trump = pos[3] > pos[4]
solver.add(after_per != after_trump)

# Answer choices: guitarist=0, keyboard player=1, saxophonist=3, trumpeter=4, violinist=5
answer_choices = [0, 1, 3, 4, 5]

# Check each answer choice
answer_index_list = []
for idx in answer_choices:
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert this role is third
    s_chk.add(pos[idx] == 3)
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)