from z3 import *

# Role indices: 0=guitarist, 1=keyboard player, 2=percussionist, 3=saxophonist, 4=trumpeter, 5=violinist
roles = ["guitarist", "keyboard player", "percussionist", "saxophonist", "trumpeter", "violinist"]
pos = {r: Int(f"pos_{i}") for i, r in enumerate(roles)}

# Base solver
solver = Solver()

# Domain constraints: each position between 1 and 6, all distinct
for i in range(6):
    solver.add(pos[roles[i]] >= 1, pos[roles[i]] <= 6)
solver.add(Distinct(*[pos[r] for r in roles]))

# Order constraints
# Guitarist does not perform the fourth solo
solver.add(pos["guitarist"] != 4)

# Percussionist before keyboard player
solver.add(pos["percussionist"] < pos["keyboard player"])

# Keyboard player after violinist and before guitarist
solver.add(pos["violinist"] < pos["keyboard player"])
solver.add(pos["keyboard player"] < pos["guitarist"])

# Saxophonist after exactly one of (percussionist, trumpeter)
sax_after_perc = pos["percussionist"] < pos["saxophonist"]
sax_after_trump = pos["trumpeter"] < pos["saxophonist"]
solver.add(Xor(sax_after_perc, sax_after_trump))

# Answer choices: ["guitarist", "keyboard player", "saxophonist", "trumpeter", "violinist"]
answer_choices = ["guitarist", "keyboard player", "saxophonist", "trumpeter", "violinist"]

# Check each answer choice
answer_index_list = []
for idx, role in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert this role performs third solo
    s_chk.add(pos[role] == 3)
    
    # If UNSAT, this role cannot perform third
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)