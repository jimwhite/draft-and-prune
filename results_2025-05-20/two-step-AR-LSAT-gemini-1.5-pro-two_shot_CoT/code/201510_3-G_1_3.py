from z3 import *

# Define variables
recruitment_order = Array('recruitment_order', IntSort(), IntSort())

# Create solver
solver = Solver()

# Constraint 1 (Domain)
i = Int('i')
solver.add(ForAll(i, Implies(And(i >= 0, i < 7), And(recruitment_order[i] >= 0, recruitment_order[i] <= 6))))

# Constraint 2 (Distinctness)
solver.add(Distinct([recruitment_order[i] for i in range(7)]))

# Constraint 3 (Stanton not before/after Tao)
i = Int('i')
solver.add(ForAll(i, Implies(And(i >= 0, i < 6), Not(Or(And(recruitment_order[i] == 3, recruitment_order[i+1] == 4), And(recruitment_order[i] == 4, recruitment_order[i+1] == 3))))))

# Constraint 4 (Quinn before Rovero)
i = Int('i')
j = Int('j')
solver.add(ForAll([i, j], Implies(And(i >= 0, i < 7, j >= 0, j < 7, recruitment_order[i] == 1, recruitment_order[j] == 2), i < j)))

# Constraint 5 (Villas immediately before White)
i = Int('i')
solver.add(ForAll(i, Implies(And(i >= 0, i < 6), Implies(recruitment_order[i] == 5, recruitment_order[i+1] == 6))))

# Constraint 6 (Peters recruited fourth)
solver.add(recruitment_order[3] == 0)

# Constraint 7 (Tao recruited second)
solver.add(recruitment_order[1] == 4)

# Check answer choices
answer_choices = [
    (1, 2),  # Quinn recruited third (index 2)
    (2, 4),  # Rovero recruited fifth (index 4)
    (3, 5),  # Stanton recruited sixth (index 5)
    (5, 5),  # Villas recruited sixth (index 5)
    (6, 2)   # White recruited third (index 2)
]

for option, (person, position) in enumerate(answer_choices):
    solver.push()
    solver.add(recruitment_order[position] == person)
    if solver.check() == sat:
        print(f"Option {chr(65 + option)} is correct")
        exit()
    solver.pop()
