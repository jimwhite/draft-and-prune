from z3 import *

# Color indices: forest=0, olive=1, peach=2, turquoise=3, white=4, yellow=5
colors = ["forest", "olive", "peach", "turquoise", "white", "yellow"]

# Rugs: each rug is a set of colors (represented as bitmasks or sets)
# We'll use Int variables to represent which colors are in each rug via bitmasks
# But for clarity, we'll use sets of Bool variables per color per rug

# Create boolean variables: used[i][c] = True if rug i uses color c
used = [[Bool(f"used_{i}_{c}") for c in range(6)] for i in range(3)]

solver = Solver()

# Global constraint: exactly 5 distinct colors used across all rugs
color_used = [Or(used[0][c], used[1][c], used[2][c]) for c in range(6)]
solver.add(Sum([If(cu, 1, 0) for cu in color_used]) == 5)

# Each rug must be either solid (size 1) or multicolored (size >=2)
# Exactly two rugs are solid, one is multicolored
rug_sizes = []
for i in range(3):
    size_i = Sum([If(used[i][c], 1, 0) for c in range(6)])
    rug_sizes.append(size_i)
    
# Exactly two rugs have size 1, one has size >=2
solid_count = Sum([If(rug_sizes[i] == 1, 1, 0) for i in range(3)])
solver.add(solid_count == 2)

# Rule constraints per rug
for i in range(3):
    # If white (4) is used, then at least 2 other colors are also used
    # i.e., if white in rug, then total size >= 3
    solver.add(Implies(used[i][4], rug_sizes[i] >= 3))
    
    # If olive (1) is used, then peach (2) must also be used
    solver.add(Implies(used[i][1], used[i][2]))
    
    # Forest (0) and turquoise (3) cannot coexist
    solver.add(Not(And(used[i][0], used[i][3])))
    
    # Peach (2) and turquoise (3) cannot coexist
    solver.add(Not(And(used[i][2], used[i][3])))
    
    # Peach (2) and yellow (5) cannot coexist
    solver.add(Not(And(used[i][2], used[i][5])))

# Answer choices: pairs of colors that are the two solid rugs
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
    
    # Enforce rug0 and rug1 are solid with colors c1 and c2 respectively
    for c in range(6):
        s_chk.add(used[0][c] == (c == c1))
        s_chk.add(used[1][c] == (c == c2))
    
    # rug2 must be multicolored (size >= 2)
    s_chk.add(rug_sizes[2] >= 2)
    
    # Ensure rug2 doesn't use c1 or c2 (disjoint colors)
    s_chk.add(Not(used[2][c1]))
    s_chk.add(Not(used[2][c2]))
    
    # Check if this configuration is possible
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)