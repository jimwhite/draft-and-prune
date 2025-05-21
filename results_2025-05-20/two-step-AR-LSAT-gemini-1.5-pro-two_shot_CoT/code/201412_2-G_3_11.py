from z3 import *

# Define constants for colors and rugs
F, O, P, T, W, Y = 0, 1, 2, 3, 4, 5
RUGS = 3
COLORS = 6

# Define variables
color_in_rug = Array('color_in_rug', IntSort(), IntSort())
rug_colors = Array('rug_colors', IntSort(), ArraySort(IntSort(), BoolSort()))

solver = Solver()

# Constraint 0: Exactly five colors are used
x = Int('x')
solver.add(Sum([If(color_in_rug[x] != -1, 1, 0) for x in range(COLORS)]) == 5)

# Constraint 1: Each used color is in exactly one rug
x = Int('x')
solver.add(ForAll([x], Implies(color_in_rug[x] != -1, And(color_in_rug[x] >= 0, color_in_rug[x] < RUGS))))

# Constraint 2: White rule
r = Int('r')
solver.add(ForAll([r], Implies(rug_colors[r][W], Sum([If(rug_colors[r][c], 1, 0) for c in range(COLORS)]) == 3)))

# Constraint 3: Olive rule
r = Int('r')
solver.add(ForAll([r], Implies(rug_colors[r][O], rug_colors[r][P])))

# Constraint 4: Forest/Turquoise rule
r = Int('r')
solver.add(ForAll([r], Not(And(rug_colors[r][F], rug_colors[r][T]))) )

# Constraint 5: Peach/Turquoise rule
r = Int('r')
solver.add(ForAll([r], Not(And(rug_colors[r][P], rug_colors[r][T]))))

# Constraint 6: Peach/Yellow rule
r = Int('r')
solver.add(ForAll([r], Not(And(rug_colors[r][P], rug_colors[r][Y]))))

# Constraint 7: Connecting color_in_rug and rug_colors
r = Int('r')
c = Int('c')
solver.add(ForAll([r, c], rug_colors[r][c] == (color_in_rug[c] == r)))

# Constraint 8: All rugs used
solver.add(And(Exists([c], color_in_rug[c] == 0), Exists([c], color_in_rug[c] == 1), Exists([c], color_in_rug[c] == 2)))


# Answer choices
choices = [
    [0, 1, 2, 2, 2, -1],  # A
    [0, 2, 2, 1, 2, -1],  # B
    [2, 1, 0, 2, 2, -1],  # C
    [-1, 2, 2, 0, -1, 1],  # D
    [1, 2, 2, -1, 0, -1]   # E
]

for i, choice in enumerate(choices):
    solver.push()
    for color, rug in enumerate(choice):
        solver.add(color_in_rug[color] == rug)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()