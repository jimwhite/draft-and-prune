from z3 import *

# Variables
solo_order = Array('solo_order', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints
# Constraint 0 (Domain)
for i in range(6):  # Iterate and add each constraint individually
    solver.add(And(solo_order[i] >= 0, solo_order[i] <= 5))
# Constraint 1 (Distinctness)
solver.add(Distinct([solo_order[i] for i in range(6)]))
# Constraint 2 (Guitarist not 4th)
solver.add(solo_order[3] != 0)
# Constraint 3 (Percussionist before Keyboard)
solver.add(Or([And(x < y, solo_order[x] == 2, solo_order[y] == 1) for x in range(6) for y in range(6)]))
# Constraint 4 (Violinist before Keyboard before Guitarist)
solver.add(Or([And(x < y, y < z, solo_order[x] == 5, solo_order[y] == 1, solo_order[z] == 0) for x in range(6) for y in range(6) for z in range(6)]))
# Constraint 5 (Saxophonist after P or T, not both)
solver.add(Or([And(solo_order[z] == 3, Xor(And(solo_order[x] == 2, x < z), And(solo_order[y] == 4, y < z))) for x in range(6) for y in range(6) for z in range(6)]))
# Constraint 6 (Percussionist before Saxophonist)
solver.add(Or([And(x < y, solo_order[x] == 2, solo_order[y] == 3) for x in range(6) for y in range(6)]))


# Answer choices
answers = [
    solo_order[0] != 2,  # A
    solo_order[1] != 2,  # B
    Or([And(x >= y, solo_order[x] == 5, solo_order[y] == 3) for x in range(6) for y in range(6)]),  # C
    Or([And(x >= y, solo_order[x] == 2, solo_order[y] == 4) for x in range(6) for y in range(6)]),  # D
    Or([And(x >= y, solo_order[x] == 3, solo_order[y] == 1) for x in range(6) for y in range(6)])  # E
]

for i, ans in enumerate(answers):
    solver.push()
    solver.add(ans)
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
