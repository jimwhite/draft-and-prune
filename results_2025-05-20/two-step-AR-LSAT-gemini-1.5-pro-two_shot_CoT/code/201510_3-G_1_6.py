from z3 import *

# Define constants for accomplice IDs
P = 0
Q = 1
R = 2
S = 3
T = 4
V = 5
W = 6

# Define the recruitment order array
recruitment_order = Array('recruitment_order', IntSort(), IntSort())

# Create the solver
solver = Solver()

# Constraint 1: Domain
i = Int('i')
solver.add(ForAll([i], Implies(And(i >= 1, i <= 7), And(recruitment_order[i] >= 0, recruitment_order[i] <= 6))))

# Constraint 2: Distinctness
solver.add(Distinct([recruitment_order[i] for i in range(1, 8)]))

# Constraint 3: Stanton not before/after Tao
i = Int('i')
solver.add(ForAll([i], Implies(And(i >= 1, i <= 7),
                               And(Implies(recruitment_order[i] == S, And(Implies(i > 1, recruitment_order[i - 1] != T),
                                                                           Implies(i < 7, recruitment_order[i + 1] != T))),
                                   Implies(recruitment_order[i] == T, And(Implies(i > 1, recruitment_order[i - 1] != S),
                                                                           Implies(i < 7, recruitment_order[i + 1] != S)))))))

# Constraint 4: Quinn before Rovero
i = Int('i')
j = Int('j')
solver.add(Exists([i, j], And(i >= 1, i <= 7, j >= 1, j <= 7, i < j, recruitment_order[i] == Q, recruitment_order[j] == R)))

# Constraint 5: Villas immediately before White
i = Int('i')
solver.add(Exists([i], And(i >= 1, i <= 6, recruitment_order[i] == V, recruitment_order[i + 1] == W)))

# Constraint 6: Peters recruited fourth
solver.add(recruitment_order[4] == P)

# Constraint 7: White immediately before Quinn
i = Int('i')
solver.add(Exists([i], And(i >= 1, i <= 6, recruitment_order[i] == W, recruitment_order[i + 1] == Q)))


# Check answer choices
answer_choices = [Q, R, S, V, W]  # Quinn, Rovero, Stanton, Villas, White
for idx, accomplice_id in enumerate(answer_choices):
    solver.push()
    solver.add(recruitment_order[6] != accomplice_id)
    if solver.check() == unsat:
        print(f"Option {chr(65 + idx)} is correct")
        exit()
    solver.pop()