from z3 import *

# Define constants for colors and rugs
F, O, P, T, W, Y = 0, 1, 2, 3, 4, 5
R1, R2, R3 = 0, 1, 2

# Define the variable
color_in_rug = Array('color_in_rug', IntSort(), IntSort())

# Create the solver
solver = Solver()

# Constraint 1: Exactly 5 colors used
solver.add(PbEq([(color_in_rug[i] != -1, 1) for i in range(6)], 5))

# Constraint 2: Each color in at most one rug
i = Int('i')
solver.add(ForAll([i], Implies(color_in_rug[i] != -1, And(color_in_rug[i] >= 0, color_in_rug[i] <= 2))))

# Constraint 3: White Rule
r = Int('r')
solver.add(ForAll([r], Implies(color_in_rug[W] == r, PbEq([(color_in_rug[i] == r, 1) for i in range(6) if i != W], 2))))

# Constraint 4: Olive Rule
solver.add(ForAll([r], Implies(color_in_rug[O] == r, color_in_rug[P] == r)))

# Constraint 5: Forest/Turquoise Rule
solver.add(ForAll([r], Not(And(color_in_rug[F] == r, color_in_rug[T] == r))))

# Constraint 6: Peach/Turquoise Rule
solver.add(ForAll([r], Not(And(color_in_rug[P] == r, color_in_rug[T] == r))))

# Constraint 7: Peach/Yellow Rule
solver.add(ForAll([r], Not(And(color_in_rug[P] == r, color_in_rug[Y] == r))))

# Answer choices
options = [
    [F, T, O, P, W, -1],  # A
    [F, T, O, P, -1, Y],  # B
    [P, T, F, O, W, -1],  # C
    [Y, F, T, O, P, -1],  # D
    [Y, O, P, T, W, -1]   # E
]

# Check each option
for opt_index, option in enumerate(options):
    solver.push()
    for color, rug in enumerate(option):
        if rug != -1:
            solver.add(color_in_rug[color] == rug // 1) # Integer division to handle potential remainders
        else:
            solver.add(color_in_rug[color] == -1)
    if solver.check() == sat:
        print(f"Option {chr(65 + opt_index)} is correct")
        exit()
    solver.pop()