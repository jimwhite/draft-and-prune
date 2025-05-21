from z3 import *

# Define variables
solo_order = Array('solo_order', IntSort(), IntSort())
idx_G, idx_K, idx_P, idx_S, idx_T, idx_V = Ints('idx_G idx_K idx_P idx_S idx_T idx_V')

solver = Solver()

# Constraint 1 & 2
for i in range(1, 7):
    solver.add(And(solo_order[i] >= 0, solo_order[i] <= 5))
solver.add(Distinct([solo_order[i] for i in range(1, 7)]))

# Constraint 3
solver.add(solo_order[idx_G] == 0)
solver.add(solo_order[idx_K] == 1)
solver.add(solo_order[idx_P] == 2)
solver.add(solo_order[idx_S] == 3)
solver.add(solo_order[idx_T] == 4)
solver.add(solo_order[idx_V] == 5)

# Constraint 4 & 5
solver.add(And(1 <= idx_G, idx_G <= 6, 1 <= idx_K, idx_K <= 6, 1 <= idx_P, idx_P <= 6, 1 <= idx_S, idx_S <= 6, 1 <= idx_T, idx_T <= 6, 1 <= idx_V, idx_V <= 6))
solver.add(Distinct(idx_G, idx_K, idx_P, idx_S, idx_T, idx_V))

# Constraint 6
solver.add(idx_G != 4)

# Constraint 7
solver.add(idx_P < idx_K)

# Constraint 8
solver.add(And(idx_V < idx_K, idx_K < idx_G))

# Constraint 9
solver.add(Xor(idx_P < idx_S, idx_T < idx_S))

# Check answer choices
musician_ids = [0, 1, 3, 4, 5]  # Corresponding to guitarist, keyboard, sax, trumpet, violin
for i, musician_id in enumerate(musician_ids):
    solver.push()
    solver.add(solo_order[3] == musician_id)
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()