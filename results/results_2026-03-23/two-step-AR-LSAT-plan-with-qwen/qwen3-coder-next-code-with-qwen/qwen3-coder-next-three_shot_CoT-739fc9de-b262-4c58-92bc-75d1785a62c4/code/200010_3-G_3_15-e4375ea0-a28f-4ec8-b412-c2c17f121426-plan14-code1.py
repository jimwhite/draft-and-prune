from z3 import *

compositions = ["F", "H", "L", "O", "P", "R", "S", "T"]
pos = {c: Int(f"pos_{c}") for c in compositions}

solver = Solver()

for c in compositions:
    solver.add(pos[c] >= 0, pos[c] <= 7)

solver.add(Distinct(*[pos[c] for c in compositions]))

solver.add(Or(pos["T"] == pos["F"] - 1, pos["T"] == pos["R"] + 1))
solver.add(Or(pos["F"] <= pos["R"] - 3, pos["F"] >= pos["R"] + 3))
solver.add(Or(pos["O"] == 0, pos["O"] == 4))
solver.add(Or(pos["L"] == 7, pos["H"] == 7))
solver.add(pos["P"] < pos["S"])
solver.add(Or(pos["O"] <= pos["S"] - 2, pos["O"] >= pos["S"] + 2))
solver.add(pos["O"] == pos["T"] + 1)
solver.add(pos["O"] == pos["R"] + 2)

solutions_F = set()

for _ in range(8):
    s_temp = Solver()
    for assertion in solver.assertions():
        s_temp.add(assertion)
    
    if solutions_F:
        s_temp.add(Or(*[pos["F"] != f for f in solutions_F]))
    
    if s_temp.check() == sat:
        m = s_temp.model()
        f_val = int(str(m.eval(pos["F"])))
        solutions_F.add(f_val)
    else:
        break

sorted_F_positions = sorted(solutions_F)

answer_choices = {
    0: {0, 1},
    1: {1, 2},
    2: {3, 5},
    3: {3, 6},
    4: {5, 6}
}

correct_choice = None
for idx, allowed_positions in answer_choices.items():
    if set(sorted_F_positions) == allowed_positions:
        correct_choice = idx
        break

if correct_choice is None:
    for idx, allowed_positions in answer_choices.items():
        if set(sorted_F_positions).issubset(allowed_positions):
            correct_choice = idx
            break

print(correct_choice)