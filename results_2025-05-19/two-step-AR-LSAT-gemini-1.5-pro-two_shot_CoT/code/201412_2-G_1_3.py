from z3 import *

# Variables
solo_order = Array('solo_order', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraint 1 (Domain)
i = Int('i')
solver.add(ForAll([i], Implies(And(i >= 1, i <= 6), And(solo_order[i] >= 0, solo_order[i] <= 5))))

# Constraint 2 (Distinctness)
solver.add(Distinct([solo_order[i] for i in range(1, 7)]))

# Constraint 3 (Guitarist not 4th)
solver.add(solo_order[4] != 0)

# Constraint 4 (Percussionist before Keyboard)
i = Int('i')
j = Int('j')
solver.add(ForAll([i, j], Implies(And(i >= 1, i <= 6, j >= 1, j <= 6, solo_order[i] == 2, solo_order[j] == 1), i < j)))

# Constraint 5 (Violinist before Keyboard before Guitarist)
i = Int('i')
j = Int('j')
k = Int('k')
solver.add(ForAll([i, j, k], Implies(And(i >= 1, i <= 6, j >= 1, j <= 6, k >= 1, k <= 6, solo_order[i] == 5, solo_order[j] == 1, solo_order[k] == 0), And(i < j, j < k)))) # Fixed: Use And() for chained comparisons

# Constraint 6 (Saxophonist after Percussionist or Trumpeter, not both)
i = Int('i')
j = Int('j')
k = Int('k')
solver.add(ForAll([i, j, k], Implies(And(i >= 1, i <= 6, j >= 1, j <= 6, k >= 1, k <= 6, solo_order[i] == 3, solo_order[j] == 2, solo_order[k] == 4), Xor(i > j, i > k))))


# Check answer choices
choices = [
    (1, 1),  # Keyboard first
    (2, 0),  # Guitarist second
    (lambda i, j: i < j, 0, 3), # Guitarist before Saxophonist
    (lambda i, j: i < j, 0, 2), # Guitarist before Percussionist
    (lambda i, j: i < j, 1, 3)  # Keyboard before Saxophonist
]

for idx, choice in enumerate(choices):
    solver.push()
    if isinstance(choice, tuple) and len(choice) == 2:
        slot, musician = choice
        solver.add(solo_order[slot] != musician)
    elif isinstance(choice, tuple) and len(choice) == 3:
        condition, musician1, musician2 = choice
        i = Int('i')
        j = Int('j')
        solver.add(ForAll([i, j], Implies(And(i >= 1, i <= 6, j >= 1, j <= 6, solo_order[i] == musician1, solo_order[j] == musician2), Not(condition(i, j)))))
    
    if solver.check() == sat:
        print(f"Option {chr(65 + idx)} is correct")
        exit()
    solver.pop()

