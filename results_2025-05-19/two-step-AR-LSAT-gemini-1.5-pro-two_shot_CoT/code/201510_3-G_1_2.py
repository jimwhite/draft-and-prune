from z3 import *

# Define variables
recruitment_order = Array('recruitment_order', IntSort(), IntSort())
i = Int('i')
j = Int('j')

# Create solver and add constraints
solver = Solver()

# Constraint 1 (Domain)
solver.add(ForAll([i], Implies(And(i >= 1, i <= 7), And(recruitment_order[i] >= 0, recruitment_order[i] <= 6))))

# Constraint 2 (Distinctness)
solver.add(Distinct([recruitment_order[i] for i in range(1, 8)]))

# Constraint 3 (Stanton not before/after Tao)
solver.add(ForAll([i], Implies(And(i >= 1, i <= 6), Not(And(recruitment_order[i] == 3, recruitment_order[i+1] == 4)))))
solver.add(ForAll([i], Implies(And(i >= 1, i <= 6), Not(And(recruitment_order[i] == 4, recruitment_order[i+1] == 3)))))

# Constraint 4 (Quinn before Rovero)
solver.add(ForAll([i, j], Implies(And(i >= 1, i <= 7, j >= 1, j <= 7, i < j, recruitment_order[i] == 1), recruitment_order[j] != 2)))


# Constraint 5 (Villas immediately before White)
solver.add(ForAll([i], Implies(And(i >= 1, i <= 6), If(recruitment_order[i] == 5, recruitment_order[i+1] == 6, True))))


# Constraint 6 (Peters recruited fourth)
solver.add(recruitment_order[4] == 0)

# Answer choices
choices = [
    [1, 3, 0, 4, 5],  # Quinn, Stanton, Peters, Tao, Villas
    [1, 3, 0, 4, 6],  # Quinn, Stanton, Peters, Tao, White
    [5, 6, 0, 1, 3],  # Villas, White, Peters, Quinn, Stanton
    [5, 6, 0, 2, 3],  # Villas, White, Peters, Rovero, Stanton
    [5, 6, 1, 2, 3]   # Villas, White, Quinn, Rovero, Stanton
]

# Check each answer choice
for idx, choice in enumerate(choices):
    solver.push()
    for i in range(5):
        solver.add(recruitment_order[i+2] == choice[i])
    if solver.check() == sat:
        print(f"Option {chr(65 + idx)} is correct")
        exit()
    solver.pop()