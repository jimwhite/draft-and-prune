from z3 import *

# Role indices: guitarist=0, keyboard player=1, percussionist=2, saxophonist=3, trumpeter=4, violinist=5
roles = ["guitarist", "keyboard player", "percussionist", "saxophonist", "trumpeter", "violinist"]
pos = [Int(f"pos_{i}") for i in range(6)]

# Base solver
solver = Solver()

# Domain constraints: each position between 1 and 6, all distinct
for i in range(6):
    solver.add(pos[i] >= 1, pos[i] <= 6)
solver.add(Distinct(*pos))

# Ordering constraints
# Guitarist does not perform the fourth solo: pos[0] != 4
solver.add(pos[0] != 4)

# Percussionist before keyboard player: pos[2] < pos[1]
solver.add(pos[2] < pos[1])

# Keyboard player after violinist and before guitarist: pos[5] < pos[1] and pos[1] < pos[0]
solver.add(pos[5] < pos[1])
solver.add(pos[1] < pos[0])

# Saxophonist after exactly one of (percussionist, trumpeter)
# (pos[3] > pos[2]) XOR (pos[3] > pos[4])
solver.add(Xor(pos[3] > pos[2], pos[3] > pos[4]))

# Answer choices: [guitarist=0, keyboard player=1, saxophonist=3, trumpeter=4, violinist=5]
answer_choices = [0, 1, 3, 4, 5]

# Check each answer choice
answer_index_list = []
for idx, role in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert this role is third
    s_chk.add(pos[role] == 3)
    
    # If UNSAT, this role cannot be third
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)