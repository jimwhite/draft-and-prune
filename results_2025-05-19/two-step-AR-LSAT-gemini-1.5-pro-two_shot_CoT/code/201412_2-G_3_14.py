from z3 import *

# Define constants for colors and rugs
F, O, P, T, W, Y = 0, 1, 2, 3, 4, 5
R1, R2, R3 = 0, 1, 2

# Define the variable
color_in_rug = Array('color_in_rug', IntSort(), IntSort())

# Create the solver
solver = Solver()

# Constraint 1: Color Usage
for c in range(6):
    solver.add(Or(color_in_rug[c] == -1, color_in_rug[c] == 0, color_in_rug[c] == 1, color_in_rug[c] == 2))

# Constraint 2: Five Colors Used
solver.add(Sum([If(color_in_rug[c] != -1, 1, 0) for c in range(6)]) == 5)

# Constraint 3: One Rug per Color
for c1 in range(6):
    for c2 in range(6):
        solver.add(Implies(And(c1 != c2, color_in_rug[c1] != -1, color_in_rug[c2] != -1), color_in_rug[c1] != color_in_rug[c2]))

# Constraint 4: White Rule
for r in range(3):
    solver.add(Implies(color_in_rug[W] == r, Sum([If(color_in_rug[c] == r, 1, 0) for c in range(6)]) == 3))

# Constraint 5: Olive Rule
solver.add(Implies(color_in_rug[O] != -1, And(color_in_rug[P] != -1, color_in_rug[O] == color_in_rug[P])))

# Constraint 6: Forest/Turquoise Rule
for r in range(3):
    solver.add(Not(And(color_in_rug[F] == r, color_in_rug[T] == r)))

# Constraint 7: Peach/Turquoise Rule
for r in range(3):
    solver.add(Not(And(color_in_rug[P] == r, color_in_rug[T] == r)))

# Constraint 8: Peach/Yellow Rule
for r in range(3):
    solver.add(Not(And(color_in_rug[P] == r, color_in_rug[Y] == r)))

# Constraint 9: Two Solid Rugs
solver.add(Sum([If(Sum([If(color_in_rug[c] == r, 1, 0) for c in range(6)]) == 1, 1, 0) for r in range(3)]) == 2)

# Answer choices
choices = [(F, P), (F, Y), (P, T), (P, Y), (T, Y)]
option_letter = 'A'

for c1, c2 in choices:
    solver.push()
    r1 = Int('r1')
    r2 = Int('r2')
    solver.add(And(r1 >= 0, r1 < 3, r2 >= 0, r2 < 3, r1 != r2,
                   Sum([If(color_in_rug[c] == r1, 1, 0) for c in range(6)]) == 1,
                   Sum([If(color_in_rug[c] == r2, 1, 0) for c in range(6)]) == 1,
                   color_in_rug[c1] == r1, color_in_rug[c2] == r2))

    if solver.check() == unsat:
        print(f"Option {option_letter} is correct")
        exit()
    solver.pop()
    option_letter = chr(ord(option_letter) + 1)