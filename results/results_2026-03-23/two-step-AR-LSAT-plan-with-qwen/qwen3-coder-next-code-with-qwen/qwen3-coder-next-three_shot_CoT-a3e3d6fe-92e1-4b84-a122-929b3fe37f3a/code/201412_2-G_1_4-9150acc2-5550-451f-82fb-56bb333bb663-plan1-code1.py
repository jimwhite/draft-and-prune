from z3 import *

# Member indices: guitar=0, keyboard=1, percussion=2, saxophone=3, trumpet=4, violinist=5
members = ["guitar", "keyboard", "percussion", "saxophone", "trumpet", "violinist"]
pos = {m: Int(f"pos_{m}") for m in members}

# Base solver
solver = Solver()

# Domain constraints: positions 1-6, all distinct
for m in members:
    solver.add(pos[m] >= 1, pos[m] <= 6)
solver.add(Distinct(*[pos[m] for m in members]))

# Guitarist constraint: does not perform fourth solo
solver.add(pos["guitar"] != 4)

# Percussion < keyboard constraint
solver.add(pos["percussion"] < pos["keyboard"])

# Violinist < keyboard < guitarist constraints
solver.add(pos["violinist"] < pos["keyboard"])
solver.add(pos["keyboard"] < pos["guitar"])

# Saxophonist XOR constraint: after exactly one of percussion or trumpeter
after_per = pos["saxophone"] > pos["percussion"]
after_tru = pos["saxophone"] > pos["trumpet"]
solver.add(Xor(after_per, after_tru))

# Answer choices: guitarist=0, keyboard=1, saxophone=3, trumpet=4, violinist=5
answer_choices = ["guitar", "keyboard", "saxophone", "trumpet", "violinist"]

# Check each answer choice
answer_index_list = []
for idx, member in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert this member performs third solo
    s_chk.add(pos[member] == 3)
    
    # If UNSAT, this member cannot be third
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)