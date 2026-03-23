from z3 import *

comps = ["F", "H", "L", "O", "P", "R", "S", "T"]
pos = {c: Int(f"pos_{c}") for c in comps}

solver = Solver()

for c in comps:
    solver.add(pos[c] >= 1, pos[c] <= 8)
solver.add(Distinct(*[pos[c] for c in comps]))

solver.add(Or(pos["O"] == 1, pos["O"] == 5))

solver.add(Or(pos["T"] + 1 == pos["F"], pos["R"] + 1 == pos["T"]))

solver.add(Or(pos["L"] == 8, pos["H"] == 8))

solver.add(pos["P"] < pos["S"])

solver.add(Or(pos["F"] + 2 <= pos["R"], pos["R"] + 2 <= pos["F"]))

solver.add(Abs(pos["O"] - pos["S"]) >= 2)

solver.add(pos["O"] == pos["T"] + 1)

solver.add(pos["O"] == 5)
solver.add(pos["T"] == 4)

feasible_F_positions = []
for f_pos in range(1, 9):
    s_chk = Solver()
    for a in solver.assertions():
        s_chk.add(a)
    s_chk.add(pos["F"] == f_pos)
    if s_chk.check() == sat:
        feasible_F_positions.append(f_pos)

answer_ranges = [
    [1, 2],
    [2, 3],
    [4, 6],
    [4, 7],
    [6, 7]
]

feasible_set = set(feasible_F_positions)

for idx, range_vals in enumerate(answer_ranges):
    choice_set = set(range(min(range_vals), max(range_vals) + 1))
    if feasible_set.issubset(choice_set):
        print(idx)
        break