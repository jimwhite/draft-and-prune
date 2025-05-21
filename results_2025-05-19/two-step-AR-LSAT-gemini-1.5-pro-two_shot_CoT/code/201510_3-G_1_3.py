from z3 import *

# Define constants for accomplice IDs
P, Q, R, S, T, V, W = 0, 1, 2, 3, 4, 5, 6

# Define the recruitment order array
recruitment_order = Array('recruitment_order', IntSort(), IntSort())

# Create the solver
solver = Solver()

# Constraint 1 (Domain)
i = Int('i')
solver.add(ForAll([i], Implies(And(i >= 1, i <= 7), And(recruitment_order[i] >= 0, recruitment_order[i] <= 6))))

# Constraint 2 (Distinctness)
solver.add(Distinct([recruitment_order[i] for i in range(1, 8)]))

# Constraint 3 (Stanton not before/after Tao)
i = Int('i')
solver.add(Or(Not(Exists([i], And(i >= 1, i <= 6, recruitment_order[i] == S, recruitment_order[i+1] == T))),
               Not(Exists([i], And(i >= 2, i <= 7, recruitment_order[i] == S, recruitment_order[i-1] == T)))))


# Constraint 4 (Quinn before Rovero)
i = Int('i')
j = Int('j')
solver.add(Exists([i, j], And(i >= 1, i <= 7, j >= 1, j <= 7, i < j, recruitment_order[i] == Q, recruitment_order[j] == R)))

# Constraint 5 (Villas before White)
i = Int('i')
solver.add(Exists([i], And(i >= 1, i <= 6, recruitment_order[i] == V, recruitment_order[i+1] == W)))

# Constraint 6 (Peters recruited fourth)
solver.add(recruitment_order[4] == P)

# Constraint 7 (Tao recruited second)
solver.add(recruitment_order[2] == T)

# Answer choices and their corresponding constraints
answer_choices = [
    (0, recruitment_order[3] == Q),  # Quinn was recruited third
    (1, recruitment_order[5] == R),  # Rovero was recruited fifth
    (2, recruitment_order[6] == S),  # Stanton was recruited sixth
    (3, recruitment_order[6] == V),  # Villas was recruited sixth
    (4, recruitment_order[3] == W)   # White was recruited third
]

# Check each answer choice
for index, constraint in answer_choices:
    solver.push()
    solver.add(constraint)
    if solver.check() == sat:
        print(f"Option {chr(65 + index)} is correct")
        exit()
    solver.pop()