from z3 import *

# Entities (integer encoding)
U, V, W, X, Y, Z = 0, 1, 2, 3, 4, 5

# Variables
band_at_slot = Array('band_at_slot', IntSort(), IntSort())

# Solver
solver = Solver()

# Base Constraints
i = Int('i')
solver.add(ForAll([i], Implies(And(i >= 0, i <= 5), And(band_at_slot[i] >= 0, band_at_slot[i] <= 5))))  # Domain
solver.add(Distinct([band_at_slot[i] for i in range(6)]))  # Distinctness
i = Int('i')
j = Int('j')
solver.add(ForAll([i, j], Implies(And(band_at_slot[i] == V, band_at_slot[j] == Z, i >= 0, i <= 5, j >= 0, j <= 5), i < j)))  # V before Z
i = Int('i')
solver.add(ForAll([i], Implies(And(band_at_slot[i] == U, i >= 0, i <= 5), i >= 3)))  # U in last three
i = Int('i')
solver.add(ForAll([i], Implies(And(band_at_slot[i] == Y, i >= 0, i <= 5), i <= 2)))  # Y in first three


# Original Constraints
i = Int('i')
j = Int('j')
solver.add(ForAll([i, j], Implies(And(band_at_slot[i] == W, band_at_slot[j] == X, i >= 0, i <= 5, j >= 0, j <= 5), i < j)))  # W before X
i = Int('i')
j = Int('j')
solver.add(ForAll([i, j], Implies(And(band_at_slot[i] == Z, band_at_slot[j] == X, i >= 0, i <= 5, j >= 0, j <= 5), i < j)))  # Z before X

original_sat = solver.check()

# Answer Choices
choices = [
    "Only Uneasy can perform in a later slot than Xpert.",
    "Vegemite performs in an earlier slot than Wellspring, which performs in an earlier slot than Zircon.",
    "Vegemite and Wellspring each perform in an earlier slot than Xpert.",
    "Xpert performs either immediately before or immediately after Uneasy.",
    "Xpert performs in either slot five or slot six."
]

for idx, choice in enumerate(choices):
    solver.push()
    if idx == 0:  # A
        i = Int('i')
        solver.add(ForAll([i], Implies(And(band_at_slot[i] != U, i >= 0, i <= 5), band_at_slot[i] <= X)))
    elif idx == 1:  # B
        i = Int('i')
        j = Int('j')
        k = Int('k')
        solver.add(ForAll([i, j, k], Implies(And(band_at_slot[i] == V, band_at_slot[j] == W, band_at_slot[k] == Z, i >= 0, i <= 5, j >= 0, j <= 5, k >= 0, k <= 5), And(i < j, j < k))))
    elif idx == 2:  # C
        i = Int('i')
        j = Int('j')
        solver.add(ForAll([i, j], Implies(And(band_at_slot[i] == V, band_at_slot[j] == X, i >= 0, i <= 5, j >= 0, j <= 5), i < j)))
        i = Int('i')
        j = Int('j')
        solver.add(ForAll([i, j], Implies(And(band_at_slot[i] == W, band_at_slot[j] == X, i >= 0, i <= 5, j >= 0, j <= 5), i < j)))
    elif idx == 3:  # D
        i = Int('i')
        solver.add(ForAll([i], Implies(And(band_at_slot[i] == X, i >= 0, i <= 5), Or(If(i < 5, band_at_slot[i + 1] == U, False), If(i > 0, band_at_slot[i - 1] == U, False)))))
    elif idx == 4:  # E
        i = Int('i')
        solver.add(ForAll([i], Implies(And(band_at_slot[i] == X, i >= 0, i <= 5), Or(i == 4, i == 5))))  # Slot 5 or 6 (index 4 or 5)

    choice_sat = solver.check()
    if original_sat == choice_sat:
        print(f"Option {chr(65 + idx)} is correct")
        exit()

    solver.pop()