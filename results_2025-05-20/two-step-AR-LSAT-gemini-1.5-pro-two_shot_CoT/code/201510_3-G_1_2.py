from z3 import *

# Define variables
recruitment_order = Array('recruitment_order', IntSort(), IntSort())

# Create solver
solver = Solver()

# Constraint 1 (Domain)
i = Int('i')
solver.add(ForAll(i, Implies(And(i >= 0, i <= 6), And(recruitment_order[i] >= 0, recruitment_order[i] <= 6))))

# Constraint 2 (Distinctness)
solver.add(Distinct([recruitment_order[i] for i in range(7)]))

# Constraint 3 (Stanton not before/after Tao)
i = Int('i')
solver.add(ForAll(i, Implies(And(i >= 0, i <= 5), Or(recruitment_order[i] != 3, recruitment_order[i+1] != 4))))
solver.add(ForAll(i, Implies(And(i >= 0, i <= 5), Or(recruitment_order[i] != 4, recruitment_order[i+1] != 3))))

# Constraint 4 (Quinn before Rovero)
q_slot = Int('q_slot') # Define q_slot and r_slot
r_slot = Int('r_slot')
solver.add(Exists([q_slot, r_slot], And(recruitment_order[q_slot] == 1, recruitment_order[r_slot] == 2, q_slot < r_slot, q_slot >= 0, q_slot <= 6, r_slot >= 0, r_slot <= 6)))


# Constraint 5 (Villas before White)
i = Int('i')
j = Int('j')
solver.add(Implies(Exists(i, And(i >= 0, i <= 6, recruitment_order[i] == 5)),
                   Exists(j, And(j > i, j <= 6, recruitment_order[j] == 6))))

# Constraint 6 (Peters recruited fourth)
solver.add(recruitment_order[3] == 0)

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
        solver.add(recruitment_order[i+1] == choice[i])
    if solver.check() == sat:
        print(f"Option {chr(65 + idx)} is correct")
        exit()
    solver.pop()

