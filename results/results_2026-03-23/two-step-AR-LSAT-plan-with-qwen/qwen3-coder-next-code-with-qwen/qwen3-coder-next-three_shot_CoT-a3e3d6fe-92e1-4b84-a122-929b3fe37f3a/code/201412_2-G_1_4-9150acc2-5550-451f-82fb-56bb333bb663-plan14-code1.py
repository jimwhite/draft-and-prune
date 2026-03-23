from z3 import *

# Role indices: guitarist=0, keyboard player=1, percussionist=2, saxophonist=3, trumpeter=4, violinist=5
roles = ["guitarist", "keyboard player", "percussionist", "saxophonist", "trumpeter", "violinist"]
pos = [Int(f"pos_{i}") for i in range(6)]

solver = Solver()

# Domain constraints: positions 1-6, all distinct
for i in range(6):
    solver.add(pos[i] >= 1, pos[i] <= 6)
solver.add(Distinct(*pos))

# Guitarist does not perform the fourth solo
solver.add(pos[0] != 4)

# Percussionist performs before keyboard player
solver.add(pos[2] < pos[1])

# Violinist before keyboard player, and keyboard player before guitarist
solver.add(pos[5] < pos[1])
solver.add(pos[1] < pos[0])

# Saxophonist performs after either percussionist or trumpeter, but not both
sax_after_per = pos[3] > pos[2]
sax_after_trump = pos[3] > pos[4]
solver.add(Or(
    And(sax_after_per, Not(sax_after_trump)),
    And(Not(sax_after_per), sax_after_trump)
))

# Answer choices: ['guitarist', 'keyboard player', 'saxophonist', 'trumpeter', 'violinist']
# Indices: guitarist=0, keyboard player=1, saxophonist=3, trumpeter=4, violinist=5
answer_choices = [0, 1, 3, 4, 5]

answer_index_list = []
for idx, role in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert this role is third
    s_chk.add(pos[role] == 3)
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)