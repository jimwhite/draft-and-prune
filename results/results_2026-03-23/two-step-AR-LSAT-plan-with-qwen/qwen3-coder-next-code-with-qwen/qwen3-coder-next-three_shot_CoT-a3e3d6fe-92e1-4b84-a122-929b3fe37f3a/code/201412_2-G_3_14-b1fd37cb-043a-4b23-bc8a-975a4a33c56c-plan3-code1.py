from z3 import *

# Color indices: forest=0, olive=1, peach=2, turquoise=3, white=4, yellow=5
COLORS = 6
color_names = ["forest", "olive", "peach", "turquoise", "white", "yellow"]

# Create solver
solver = Solver()

# Boolean variables: used[color] indicates if color is used in any rug
used = [Bool(f"used_{i}") for i in range(COLORS)]

# Exactly five colors used
solver.add(Sum([If(used[i], 1, 0) for i in range(COLORS)]) == 5)

# Rug variables: R0, R1, R2
RUGS = 3

# Boolean variables for whether each rug is solid
solid = [Bool(f"R{i}_solid") for i in range(RUGS)]

# Exactly two solid rugs
solver.add(Sum([If(solid[i], 1, 0) for i in range(RUGS)]) == 2)

# c[r][color] = True if color is used in rug r
c = [[Bool(f"c_{r}_{i}") for i in range(COLORS)] for r in range(RUGS)]

# Mutual exclusivity: each color appears in at most one rug
for i in range(COLORS):
    solver.add(Sum([If(c[r][i], 1, 0) for r in range(RUGS)]) <= 1)

# Global usage: used[i] = OR of c[r][i] over rugs
for i in range(COLORS):
    solver.add(used[i] == Or([c[r][i] for r in range(RUGS)]))

# Solid rug constraints: if solid, exactly one color; else at least two colors
for r in range(RUGS):
    # If solid, exactly one color used in rug
    solver.add(Implies(solid[r], Sum([If(c[r][i], 1, 0) for i in range(COLORS)]) == 1))
    # If not solid, at least two colors
    solver.add(Implies(Not(solid[r]), Sum([If(c[r][i], 1, 0) for i in range(COLORS)]) >= 2))

# Rule constraints per rug
for r in range(RUGS):
    # If white is used, then at least 3 colors (white + 2 others)
    solver.add(Implies(c[r][4], Sum([If(c[r][i], 1, 0) for i in range(COLORS)]) >= 3))
    
    # If olive is used, then peach must also be used in same rug
    solver.add(Implies(c[r][1], c[r][2]))
    
    # Forest and turquoise cannot both appear in same rug
    solver.add(Not(And(c[r][0], c[r][3])))
    
    # Peach and turquoise cannot both appear in same rug
    solver.add(Not(And(c[r][2], c[r][3])))
    
    # Peach and yellow cannot both appear in same rug
    solver.add(Not(And(c[r][2], c[r][5])))

# Answer choices: pairs of colors that cannot be the two solid rugs
answer_choices = [
    (0, 2),  # forest and peach
    (0, 5),  # forest and yellow
    (2, 3),  # peach and turquoise
    (2, 5),  # peach and yellow
    (3, 5)   # turquoise and yellow
]

answer_index_list = []

for idx, (c1, c2) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assume rugs 0 and 1 are solid, rug 2 is multicolored (WLOG due to symmetry)
    s_chk.add(solid[0] == True, solid[1] == True, solid[2] == False)
    
    # Rug 0 is solid with color c1
    for i in range(COLORS):
        if i == c1:
            s_chk.add(c[0][i] == True)
        else:
            s_chk.add(c[0][i] == False)
    
    # Rug 1 is solid with color c2
    for i in range(COLORS):
        if i == c2:
            s_chk.add(c[1][i] == True)
        else:
            s_chk.add(c[1][i] == False)
    
    # Check if this configuration is possible
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)