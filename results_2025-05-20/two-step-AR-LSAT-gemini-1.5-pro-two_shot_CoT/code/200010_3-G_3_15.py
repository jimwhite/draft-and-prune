from z3 import *

# Define variables
composition_at_slot = Array('composition_at_slot', IntSort(), IntSort())
idx_of_composition = Array('idx_of_composition', IntSort(), IntSort())

solver = Solver()

# Constraint 0 (Inverse Mapping)
i = Int('i')
j = Int('j')
solver.add(ForAll([i], Implies(And(i >= 0, i <= 7), idx_of_composition[composition_at_slot[i]] == i)))
solver.add(ForAll([j], Implies(And(j >= 0, j <= 7), composition_at_slot[idx_of_composition[j]] == j)))


# Constraint 1 (Domain and Distinctness)
solver.add(Distinct([composition_at_slot[i] for i in range(8)]))
solver.add(ForAll([i], Implies(And(i >= 0, i <= 7), And(composition_at_slot[i] >= 0, composition_at_slot[i] <= 7))))

# Constraint 2 (T before F or after R)
solver.add(Or(idx_of_composition[7] + 1 == idx_of_composition[0], idx_of_composition[7] - 1 == idx_of_composition[5]))

# Constraint 3 (Two between F and R)
solver.add(Or(And(idx_of_composition[0] < idx_of_composition[5], idx_of_composition[5] - idx_of_composition[0] - 1 >= 2),
               And(idx_of_composition[5] < idx_of_composition[0], idx_of_composition[0] - idx_of_composition[5] - 1 >= 2)))

# Constraint 4 (O first or fifth)
solver.add(Or(idx_of_composition[3] == 0, idx_of_composition[3] == 4))

# Constraint 5 (L or H eighth)
solver.add(Or(idx_of_composition[2] == 7, idx_of_composition[1] == 7))

# Constraint 6 (P before S)
solver.add(idx_of_composition[4] < idx_of_composition[6])

# Constraint 7 (One between O and S)
solver.add(Or(And(idx_of_composition[3] < idx_of_composition[6], idx_of_composition[6] - idx_of_composition[3] - 1 >= 1),
               And(idx_of_composition[6] < idx_of_composition[3], idx_of_composition[3] - idx_of_composition[6] - 1 >= 1)))

# Constraint 8 (O after T)
solver.add(idx_of_composition[3] == idx_of_composition[7] + 1)

# Check answer choices
answer_choices = [
    Or(idx_of_composition[0] == 0, idx_of_composition[0] == 1),  # first or second
    Or(idx_of_composition[0] == 1, idx_of_composition[0] == 2),  # second or third
    Or(idx_of_composition[0] == 3, idx_of_composition[0] == 5),  # fourth or sixth
    Or(idx_of_composition[0] == 3, idx_of_composition[0] == 6),  # fourth or seventh
    Or(idx_of_composition[0] == 5, idx_of_composition[0] == 6)   # sixth or seventh
]

for i, choice in enumerate(answer_choices):
    solver.push()
    solver.add(Not(choice))
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()