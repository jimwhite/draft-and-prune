from z3 import *

# Define constants for colors and rugs
F, O, P, T, W, Y = 0, 1, 2, 3, 4, 5
R1, R2, R3 = 0, 1, 2

# Define the variable
color_in_rug = Array('color_in_rug', IntSort(), IntSort())

# Create the solver
solver = Solver()

# Constraint 0: Exactly five colors are used
solver.add(Sum([If(color_in_rug[i] != -1, 1, 0) for i in range(6)]) == 5)

# Constraint 1: Each used color is in exactly one rug
solver.add(And([Implies(color_in_rug[i] != -1, And(color_in_rug[i] >= 0, color_in_rug[i] <= 2)) for i in range(6)]))


# Constraint 2: White rule
solver.add(Implies(color_in_rug[W] != -1, Sum([If(color_in_rug[i] == color_in_rug[W], 1, 0) for i in range(6)]) == 3))

# Constraint 3: Olive/Peach rule
solver.add(Implies(color_in_rug[O] != -1, And(color_in_rug[P] != -1, color_in_rug[O] == color_in_rug[P])))

# Constraint 4: Forest/Turquoise rule
solver.add(Implies(And(color_in_rug[F] != -1, color_in_rug[T] != -1), color_in_rug[F] != color_in_rug[T]))

# Constraint 5: Peach/Turquoise rule
solver.add(Implies(And(color_in_rug[P] != -1, color_in_rug[T] != -1), color_in_rug[P] != color_in_rug[T]))

# Constraint 6: Peach/Yellow rule
solver.add(Implies(And(color_in_rug[P] != -1, color_in_rug[Y] != -1), color_in_rug[P] != color_in_rug[Y]))


# Check answer choices
answer_choices = [
    Implies(color_in_rug[F] != -1, Sum([If(color_in_rug[i] == color_in_rug[F], 1, 0) for i in range(6)]) > 1),  # A
    Implies(color_in_rug[T] != -1, Sum([If(color_in_rug[i] == color_in_rug[T], 1, 0) for i in range(6)]) > 1),  # B
    color_in_rug[P] == -1,  # C
    color_in_rug[T] == -1,  # D
    color_in_rug[Y] == -1   # E
]

for i, choice in enumerate(answer_choices):
    solver.push()
    solver.add(choice)
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()