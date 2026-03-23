from z3 import *

# Color indices: forest=0, olive=1, peach=2, turquoise=3, white=4, yellow=5
colors = ["forest", "olive", "peach", "turquoise", "white", "yellow"]

# Create solver
solver = Solver()

# For each rug and color, binary variable indicating if the color is used in that rug
# Rugs: 0 and 1 are solid, 2,3,4 are multicolored
c = [[Bool(f"c_{r}_{col}") for col in range(6)] for r in range(5)]

# Exactly 5 colors total used (one color unused)
color_used = [Or([c[r][col] for r in range(5)]) for col in range(6)]
solver.add(Sum([If(col_used, 1, 0) for col_used in color_used]) == 5)

# Solid rugs: each uses exactly one color
for r in [0, 1]:
    solver.add(Sum([If(c[r][col], 1, 0) for col in range(6)]) == 1)

# Multicolored rugs: each uses at least 2 colors
for r in [2, 3, 4]:
    solver.add(Sum([If(c[r][col], 1, 0) for col in range(6)]) >= 2)

# No color appears in more than one rug
for col in range(6):
    solver.add(Sum([If(c[r][col], 1, 0) for r in range(5)]) <= 1)

# Rule: If white is used in a rug, two other colors are also used (i.e., rug has exactly 3 colors)
for r in range(5):
    # If white is used, then rug has exactly 3 colors
    solver.add(Implies(c[r][4], Sum([If(c[r][col], 1, 0) for col in range(6)]) == 3))

# Rule: If olive is used, peach must also be used in the same rug
for r in range(5):
    solver.add(Implies(c[r][1], c[r][2]))

# Rule: Forest and turquoise not used together
for r in range(5):
    solver.add(Not(And(c[r][0], c[r][3])))

# Rule: Peach and turquoise not used together
for r in range(5):
    solver.add(Not(And(c[r][2], c[r][3])))

# Rule: Peach and yellow not used together
for r in range(5):
    solver.add(Not(And(c[r][2], c[r][5])))

# Answer choices: pairs of colors for the two solid rugs
answer_choices = [
    (0, 2),  # forest and peach
    (0, 5),  # forest and yellow
    (2, 3),  # peach and turquoise
    (2, 5),  # peach and yellow
    (3, 5)   # turquoise and yellow
]

# Check each answer choice
answer_index_list = []
for idx, (col1, col2) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Fix the two solid rugs to use exactly these colors
    s_chk.add(c[0][col1] == True)
    s_chk.add(c[1][col2] == True)
    
    # Ensure no other colors in these solid rugs
    for col in range(6):
        if col != col1:
            s_chk.add(c[0][col] == False)
        if col != col2:
            s_chk.add(c[1][col] == False)
    
    # Check feasibility
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)