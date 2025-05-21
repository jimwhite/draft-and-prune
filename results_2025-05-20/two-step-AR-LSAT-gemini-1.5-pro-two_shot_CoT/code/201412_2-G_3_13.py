from z3 import *

# Define constants for colors and rugs
F, O, P, T, W, Y = 0, 1, 2, 3, 4, 5
RUGS = 3
COLORS = 6

# Define variables
color_in_rug = Array('color_in_rug', IntSort(), IntSort())
rug_colors = Array('rug_colors', IntSort(), IntSort())

solver = Solver()

# Constraint 1: Color Assignment
x = Int('x')
solver.add(ForAll([x], Implies(And(x >= 0, x < COLORS), Or(And(color_in_rug[x] >= 0, color_in_rug[x] < RUGS), color_in_rug[x] == -1))))

# Constraint 2: Five Colors Used
# Corrected: PbEq takes a list of tuples (BoolRef, weight)
solver.add(PbEq([(color_in_rug[i] != -1, 1) for i in range(COLORS)], 5))

# Constraint 3: Rug Color Counts Definition
for r in range(RUGS):
    solver.add(rug_colors[r] == Sum([If(color_in_rug[c] == r, 1, 0) for c in range(COLORS)]))

# Constraint 4: Rug Size Limits
r = Int('r')
solver.add(ForAll([r], Implies(And(r >= 0, r < RUGS), And(rug_colors[r] >= 1, rug_colors[r] <= 3))))

# Constraint 5: White Rule
solver.add(Implies(color_in_rug[W] != -1, rug_colors[color_in_rug[W]] == 3))

# Constraint 6: Olive Rule
solver.add(Implies(color_in_rug[O] != -1, And(color_in_rug[P] != -1, color_in_rug[O] == color_in_rug[P])))

# Constraint 7: Forest/Turquoise Rule
solver.add(Implies(And(color_in_rug[F] != -1, color_in_rug[T] != -1), color_in_rug[F] != color_in_rug[T]))

# Constraint 8: Peach/Turquoise Rule
solver.add(Implies(And(color_in_rug[P] != -1, color_in_rug[T] != -1), color_in_rug[P] != color_in_rug[T]))

# Constraint 9: Peach/Yellow Rule
solver.add(Implies(And(color_in_rug[P] != -1, color_in_rug[Y] != -1), color_in_rug[P] != color_in_rug[Y]))

# Constraint 10: Solid Peach Rug
solver.add(color_in_rug[P] != -1)
solver.add(rug_colors[color_in_rug[P]] == 1)


# Check answer choices
negations = [
    Implies(color_in_rug[F] != -1, rug_colors[color_in_rug[F]] != 1),
    Implies(color_in_rug[T] != -1, rug_colors[color_in_rug[T]] != 1),
    Implies(color_in_rug[Y] != -1, rug_colors[color_in_rug[Y]] != 1),
    Not(And(color_in_rug[F] != -1, color_in_rug[W] != -1, color_in_rug[F] == color_in_rug[W])),
    Not(And(color_in_rug[W] != -1, color_in_rug[Y] != -1, color_in_rug[W] == color_in_rug[Y]))
]

for i, neg in enumerate(negations):
    solver.push()
    solver.add(neg)
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()

