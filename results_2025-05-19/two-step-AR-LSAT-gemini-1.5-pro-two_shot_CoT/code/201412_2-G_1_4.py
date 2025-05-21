from z3 import *

# Define variables
solo_order = Array('solo_order', IntSort(), IntSort())

# Create solver
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
solver.add(Exists([i, j], And(i >= 1, i <= 6, j >= 1, j <= 6, i < j, solo_order[i] == 2, solo_order[j] == 1)))

# Constraint 5 (Violinist before Keyboard before Guitarist)
i = Int('i')
j = Int('j')
k = Int('k')
solver.add(Exists([i, j, k], And(i >= 1, i <= 6, j >= 1, j <= 6, k >= 1, k <= 6, i < j, j < k, solo_order[i] == 5, solo_order[j] == 1, solo_order[k] == 0)))

# Constraint 6 (Saxophonist after Percussionist or Trumpeter, not both)
i = Int('i')
j = Int('j')
solver.add(Or(
    And(Exists([i, j], And(i >= 1, i <= 6, j >= 1, j <= 6, i < j, solo_order[i] == 2, solo_order[j] == 3)),
        Not(Exists([i, j], And(i >= 1, i <= 6, j >= 1, j <= 6, i < j, solo_order[i] == 4, solo_order[j] == 3)))),
    And(Exists([i, j], And(i >= 1, i <= 6, j >= 1, j <= 6, i < j, solo_order[i] == 4, solo_order[j] == 3)),
        Not(Exists([i, j], And(i >= 1, i <= 6, j >= 1, j <= 6, i < j, solo_order[i] == 2, solo_order[j] == 3))))
))

# Check answer choices
musicians = ["guitarist", "keyboard player", "saxophonist", "trumpeter", "violinist"]
for idx, musician in enumerate(musicians):
    solver.push()
    solver.add(solo_order[3] == idx)
    if solver.check() == unsat:
        print(f"Option {chr(65 + idx)} is correct")
        exit()
    solver.pop()