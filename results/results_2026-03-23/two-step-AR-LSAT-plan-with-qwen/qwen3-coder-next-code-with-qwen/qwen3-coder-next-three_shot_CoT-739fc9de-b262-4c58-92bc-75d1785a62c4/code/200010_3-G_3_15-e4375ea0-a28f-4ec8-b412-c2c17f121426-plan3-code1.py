from z3 import *

compositions = ["F", "H", "L", "O", "P", "R", "S", "T"]
pos = {c: Int(f"pos_{c}") for c in compositions}

solver = Solver()

for c in compositions:
    solver.add(pos[c] >= 0, pos[c] <= 7)

solver.add(Distinct(*[pos[c] for c in compositions]))

solver.add(Or(pos["T"] + 1 == pos["F"], pos["R"] + 1 == pos["T"]))

solver.add(Or(pos["F"] <= pos["R"] - 3, pos["R"] <= pos["F"] - 3))

solver.add(Or(pos["O"] == 0, pos["O"] == 4))

solver.add(Or(pos["L"] == 7, pos["H"] == 7))

solver.add(pos["P"] < pos["S"])

solver.add(Or(pos["O"] <= pos["S"] - 2, pos["S"] <= pos["O"] - 2))

solver.add(pos["O"] == pos["T"] + 1)

solver.add(pos["O"] == 4)
solver.add(pos["T"] == 3)

solver.add(pos["R"] == 2)

possible_F_indices = []
for candidate in [5, 6]:
    s = Solver()
    for a in solver.assertions():
        s.add(a)
    s.add(pos["F"] == candidate)
    
    if s.check() == sat:
        possible_F_indices.append(candidate)

if possible_F_indices == [5, 6]:
    print("sixth or seventh")
elif possible_F_indices == [5]:
    print("sixth")
elif possible_F_indices == [6]:
    print("seventh")
else:
    for candidate in range(8):
        if candidate in [2, 3, 4]:
            continue
        s = Solver()
        for a in solver.assertions():
            s.add(a)
        s.add(pos["F"] == candidate)
        if s.check() == sat:
            print(f"Found possible F at index {candidate}")