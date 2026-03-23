from z3 import *

# Compositions: F, H, L, O, P, R, S, T
comps = ["F", "H", "L", "O", "P", "R", "S", "T"]
pos = {c: Int(f"pos_{c}") for c in comps}

solver = Solver()

# Domain constraints: positions 1-8, all distinct
for c in comps:
    solver.add(pos[c] >= 1, pos[c] <= 8)
solver.add(Distinct(*[pos[c] for c in comps]))

# T is performed either immediately before F or immediately after R
solver.add(Or(pos["T"] + 1 == pos["F"], pos["R"] + 1 == pos["T"]))

# At least two compositions between F and R
solver.add(Or(pos["F"] + 2 <= pos["R"], pos["R"] + 2 <= pos["F"]))

# O is performed either first or fifth
solver.add(Or(pos["O"] == 1, pos["O"] == 5))

# Eighth composition is L or H
solver.add(Or(pos["L"] == 8, pos["H"] == 8))

# P before S
solver.add(pos["P"] < pos["S"])

# At least one composition between O and S
solver.add(Or(pos["O"] + 1 == pos["S"], pos["S"] + 1 == pos["O"], 
             pos["O"] + 2 <= pos["S"], pos["S"] + 2 <= pos["O"]))

# Premise: O is performed immediately after T
solver.add(pos["T"] + 1 == pos["O"])

# Answer choices as sets of positions
answer_choices = [
    {1, 2},      # first or second
    {2, 3},      # second or third
    {4, 6},      # fourth or sixth
    {4, 7},      # fourth or seventh
    {6, 7}       # sixth or seventh
]

answer_index_list = []
for idx, choice_set in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert F is NOT in this choice set
    s_chk.add(And(*[pos["F"] != p for p in choice_set]))
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)