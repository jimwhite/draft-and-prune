from z3 import *

# 1. Entities (as defined in the plan)
P = 0
Q = 1
R = 2
S = 3
T = 4
V = 5
W = 6

# 2. Variables
recruitment_order = Array('recruitment_order', IntSort(), IntSort())
i = Int('i')
q_slot = Int('q_slot')
r_slot = Int('r_slot')
v_slot = Int('v_slot')
w_slot = Int('w_slot')
t_slot = Int('t_slot')


# Solver
solver = Solver()

# 3. Base Constraints
solver.add(ForAll([i], Implies(And(i >= 1, i <= 7), And(recruitment_order[i] >= 0, recruitment_order[i] <= 6))))
solver.add(Distinct([recruitment_order[i] for i in range(1, 8)]))
solver.add(ForAll([i], Implies(And(i >= 1, i <= 6), Or(recruitment_order[i] != S, recruitment_order[i+1] != T))))
solver.add(ForAll([i], Implies(And(i >= 2, i <= 7), Or(recruitment_order[i] != S, recruitment_order[i-1] != T))))
solver.add(Exists([q_slot, r_slot], And(recruitment_order[q_slot] == Q, recruitment_order[r_slot] == R, q_slot < r_slot, q_slot >= 1, q_slot <= 7, r_slot >= 1, r_slot <= 7)))
solver.add(Exists([v_slot], And(v_slot >= 1, v_slot <= 6, recruitment_order[v_slot] == V, recruitment_order[v_slot + 1] == W)))
solver.add(recruitment_order[4] == P)


# 4. Conditional Constraints
solver.add(Exists([w_slot, r_slot], And(recruitment_order[w_slot] == W, recruitment_order[r_slot] == R, w_slot < r_slot, w_slot >= 1, w_slot <= 7, r_slot >= 1, r_slot <= 7)))
solver.add(Exists([r_slot, t_slot], And(recruitment_order[r_slot] == R, recruitment_order[t_slot] == T, r_slot < t_slot, r_slot >= 1, r_slot <= 7, t_slot >= 1, t_slot <= 7)))


# 5. Answer Choices
answer_choices = [
    (Q, 1),  # A: Quinn was recruited first
    (R, 3),  # B: Rovero was recruited third
    (S, 2),  # C: Stanton was recruited second
    (T, 6),  # D: Tao was recruited sixth
    (V, 6)   # E: Villas was recruited sixth
]

for option, (accomplice, slot) in enumerate(answer_choices):
    solver.push()
    solver.add(recruitment_order[slot] == accomplice)
    if solver.check() == sat:
        print(f"Option {chr(65 + option)} is correct")
        exit()
    solver.pop()