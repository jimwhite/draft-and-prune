from z3 import *

# 1. Define constants for accomplices
P, Q, R, S, T, V, W = 0, 1, 2, 3, 4, 5, 6
accomplices = [P, Q, R, S, T, V, W]

# 2. Define the recruitment_order array
recruitment_order = Array('recruitment_order', IntSort(), IntSort())

# 3. Formulate constraints
solver = Solver()

# Constraint 1: Domain
for i in range(7):
    solver.add(recruitment_order[i] >= 0, recruitment_order[i] <= 6)

# Constraint 2: Distinctness
solver.add(Distinct([recruitment_order[i] for i in range(7)]))

# Constraint 3: Stanton not adjacent to Tao
for i in range(6):
    solver.add(Not(And(recruitment_order[i] == S, recruitment_order[i+1] == T)))
    solver.add(Not(And(recruitment_order[i] == T, recruitment_order[i+1] == S)))

# Constraint 4: Quinn before Rovero
q_idx = Int('q_idx')
r_idx = Int('r_idx')
solver.add(q_idx >= 0, q_idx < 7)
solver.add(r_idx >= 0, r_idx < 7)
solver.add(recruitment_order[q_idx] == Q)
solver.add(recruitment_order[r_idx] == R)
solver.add(q_idx < r_idx)


# Constraint 5: Villas immediately before White
v_idx = Int('v_idx')
solver.add(v_idx >= 0, v_idx < 6)
solver.add(recruitment_order[v_idx] == V)
solver.add(recruitment_order[v_idx + 1] == W)

# Constraint 6: Peters recruited fourth
solver.add(recruitment_order[3] == P)

# 4. Create solver and assert constraints (already done above)

# 5. Check answer choices
choices = [
    [Q, T, S, P, V, W, R],
    [Q, W, R, P, S, V, T],
    [V, W, Q, S, P, T, R],
    [V, W, S, P, Q, T, R],
    [V, W, S, P, R, T, Q]
]

for i, choice in enumerate(choices):
    solver.push()
    for j in range(7):
        solver.add(recruitment_order[j] == choice[j])
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()