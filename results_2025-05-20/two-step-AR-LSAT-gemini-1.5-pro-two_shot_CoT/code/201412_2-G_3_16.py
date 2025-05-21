from z3 import *

# Define constants for colors and rugs
F, O, P, T, W, Y = 0, 1, 2, 3, 4, 5
RUGS = range(3)
COLORS = range(6)

# Define Z3 variables
color_in_rug = Array('color_in_rug', IntSort(), IntSort())
num_colors_in_rug = Array('num_colors_in_rug', IntSort(), IntSort())

solver = Solver()

# Constraint 1: Color Usage
for c in COLORS:
    solver.add(Or(And(color_in_rug[c] >= 0, color_in_rug[c] <= 2), color_in_rug[c] == -1))

# Constraint 2: Five Colors Used
solver.add(Sum([If(color_in_rug[c] != -1, 1, 0) for c in COLORS]) == 5)

# Constraint 3: One Rug per Color
for c1 in COLORS:
    for c2 in COLORS:
        solver.add(Implies(And(c1 != c2, color_in_rug[c1] != -1, color_in_rug[c2] != -1), color_in_rug[c1] != color_in_rug[c2]))

# Constraint 4: White Rule
for r in RUGS:
    solver.add(Implies(color_in_rug[W] == r, num_colors_in_rug[r] == 3))

# Constraint 5: Olive Rule
for r in RUGS:
    solver.add(Implies(color_in_rug[O] == r, color_in_rug[P] == r))

# Constraint 6: Forest/Turquoise Rule
for r in RUGS:
    solver.add(Not(And(color_in_rug[F] == r, color_in_rug[T] == r)))

# Constraint 7: Peach/Turquoise Rule
for r in RUGS:
    solver.add(Not(And(color_in_rug[P] == r, color_in_rug[T] == r)))

# Constraint 8: Peach/Yellow Rule
for r in RUGS:
    solver.add(Not(And(color_in_rug[P] == r, color_in_rug[Y] == r)))

# Constraint 9: Num Colors in Rug Calculation
for r in RUGS:
    solver.add(num_colors_in_rug[r] == Sum([If(color_in_rug[c] == r, 1, 0) for c in COLORS]))

# Constraint 10: Solid Yellow Rug
solver.add(Or([And(color_in_rug[Y] == r, num_colors_in_rug[r] == 1) for r in RUGS]))


# Check answer choices
answer_choices = [
    Sum([If(num_colors_in_rug[r] == 1, 1, 0) for r in RUGS]) == 1,  # A
    Or([And(color_in_rug[F] == r, num_colors_in_rug[r] == 1) for r in RUGS]),  # B
    color_in_rug[T] == -1,  # C
    Or([And(color_in_rug[F] == r, color_in_rug[O] == r) for r in RUGS]),  # D
    Or([And(color_in_rug[P] == r, color_in_rug[W] == r) for r in RUGS])  # E
]

for i, choice in enumerate(answer_choices):
    solver.push()
    solver.add(choice)
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()