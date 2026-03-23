from z3 import *

roles = ["guitarist", "keyboard player", "percussionist", "saxophonist", "trumpeter", "violinist"]
pos = [Int(f"pos_{i}") for i in range(6)]

solver = Solver()

for i in range(6):
    solver.add(pos[i] >= 1, pos[i] <= 6)
solver.add(Distinct(*pos))

solver.add(pos[0] != 4)

solver.add(pos[2] < pos[1])

solver.add(pos[5] < pos[1])
solver.add(pos[1] < pos[0])

solver.add((pos[2] < pos[3]) != (pos[4] < pos[3]))

answer_choices = [0, 1, 3, 4, 5]

answer_index_list = []
for idx in answer_choices:
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    s_chk.add(pos[idx] == 3)
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)