from z3 import *

# Variables
composition_at_slot = Array('composition_at_slot', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints
# Constraint 0 (Domain)
for i in range(8):
    solver.add(composition_at_slot[i] >= 0, composition_at_slot[i] <= 7)

# Constraint 1 (Distinctness)
solver.add(Distinct([composition_at_slot[i] for i in range(8)]))

# Constraint 2 (T before F or after R)
solver.add(Or(Exists([k], And(composition_at_slot[k] == 7, ForAll([j], Implies(composition_at_slot[j] == 0, j > k)))),
               Exists([k], And(composition_at_slot[k] == 5, ForAll([j], Implies(composition_at_slot[j] == 7, j > k)))))


# Constraint 3 (Two between F and R)
f_index = Sum([If(composition_at_slot[j] == 0, j, 8) for j in range(8)])
r_index = Sum([If(composition_at_slot[j] == 5, j, 8) for j in range(8)])
solver.add(Or(Sum([If(And(i > f_index, i < r_index), 1, 0) for i in range(8)]) == 2,
               Sum([If(And(i > r_index, i < f_index), 1, 0) for i in range(8)]) == 2))

# Constraint 4 (O first or fifth)
solver.add(Or(composition_at_slot[0] == 3, composition_at_slot[4] == 3))

# Constraint 5 (L or H eighth)
solver.add(Or(composition_at_slot[7] == 2, composition_at_slot[7] == 1))

# Constraint 6 (P before S)
solver.add(Sum([If(composition_at_slot[i] == 4, i, 8) for i in range(8)]) < Sum([If(composition_at_slot[i] == 6, i, 8) for i in range(8)]))

# Constraint 7 (One between O and S)
o_index = Sum([If(composition_at_slot[j] == 3, j, 8) for j in range(8)])
s_index = Sum([If(composition_at_slot[j] == 6, j, 8) for j in range(8)])
solver.add(Or(Sum([If(And(i > o_index, i < s_index), 1, 0) for i in range(8)]) == 1,
               Sum([If(And(i > s_index, i < o_index), 1, 0) for i in range(8)]) == 1))

# Constraint 8 (S is fourth)
solver.add(composition_at_slot[3] == 6)

# Answer Choices
options = [
    [0, 1, 4],  # F, H, P
    [1, 4, 2],  # H, P, L
    [3, 4, 5],  # O, P, R
    [3, 4, 7],  # O, P, T
    [4, 5, 7]   # P, R, T
]

for i, option in enumerate(options):
    solver.push()
    solver.add(composition_at_slot[0] == option[0])
    solver.add(composition_at_slot[1] == option[1])
    solver.add(composition_at_slot[2] == option[2])
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
