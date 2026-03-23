from z3 import *

# Color indices: forest=0, olive=1, peach=2, turquoise=3, white=4, yellow=5
colors = 6

# Variables
use = [Bool(f"use_{c}") for c in range(colors)]
solid = [Bool(f"solid_{r}") for r in range(3)]
color_in_rug = [[Bool(f"color_in_rug_{r}_{c}") for c in range(colors)] for r in range(3)]

solver = Solver()

# Exactly 5 colors used
solver.add(Sum([If(use[c], 1, 0) for c in range(colors)]) == 5)

# Color usage consistency: use[c] iff at least one rug uses color c
for c in range(colors):
    solver.add(use[c] == Or([color_in_rug[r][c] for r in range(3)]))

# Solid/multicolored constraints
for r in range(3):
    # If solid, exactly one color used
    solver.add(Implies(solid[r], Sum([If(color_in_rug[r][c], 1, 0) for c in range(colors)]) == 1))
    # If not solid (multicolored), at least two colors used
    solver.add(Implies(Not(solid[r]), Sum([If(color_in_rug[r][c], 1, 0) for c in range(colors)]) >= 2))

# Exactly two solid rugs
solver.add(Sum([If(solid[r], 1, 0) for r in range(3)]) == 2)

# Rule: In any rug with white, exactly two other colors are used
for r in range(3):
    solver.add(Implies(color_in_rug[r][4], 
                       Sum([If(color_in_rug[r][c], 1, 0) for c in range(colors) if c != 4]) == 2))

# Rule: If olive is used in a rug, peach must also be used
for r in range(3):
    solver.add(Implies(color_in_rug[r][1], color_in_rug[r][2]))

# Rule: Forest and turquoise not used together
for r in range(3):
    solver.add(Not(And(color_in_rug[r][0], color_in_rug[r][3])))

# Rule: Peach and turquoise not used together
for r in range(3):
    solver.add(Not(And(color_in_rug[r][2], color_in_rug[r][3])))

# Rule: Peach and yellow not used together
for r in range(3):
    solver.add(Not(And(color_in_rug[r][2], color_in_rug[r][5])))

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
    
    # Try to assign two solid rugs with colors c1 and c2
    # We'll try all possible assignments of which rug gets which color
    found_sat = False
    
    for r1 in range(3):
        for r2 in range(3):
            if r1 == r2:
                continue
            
            s_chk.push()
            
            # Set rug r1 as solid with color c1
            s_chk.add(solid[r1])
            for c in range(colors):
                if c == c1:
                    s_chk.add(color_in_rug[r1][c])
                else:
                    s_chk.add(Not(color_in_rug[r1][c]))
            
            # Set rug r2 as solid with color c2
            s_chk.add(solid[r2])
            for c in range(colors):
                if c == c2:
                    s_chk.add(color_in_rug[r2][c])
                else:
                    s_chk.add(Not(color_in_rug[r2][c]))
            
            # The third rug must be multicolored
            r3 = 3 - r1 - r2  # This doesn't work for arbitrary r1, r2
            # Let's find the third rug index properly
            rugs = [0, 1, 2]
            r3_list = [r for r in rugs if r != r1 and r != r2]
            if len(r3_list) == 0:
                s_chk.pop()
                continue
            r3 = r3_list[0]
            s_chk.add(Not(solid[r3]))
            
            # Check satisfiability
            if s_chk.check() == sat:
                found_sat = True
            
            s_chk.pop()
    
    # If no assignment works, this pair cannot be the two solid rugs
    if not found_sat:
        answer_index_list.append(idx)

print(answer_index_list)