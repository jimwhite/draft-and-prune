from z3 import *

# Color indices: forest=0, olive=1, peach=2, turquoise=3, white=4, yellow=5
COLORS = 6
color_names = ["forest", "olive", "peach", "turquoise", "white", "yellow"]

# Use variables: which colors are used (exactly 5)
use = [Bool(f"use_{c}") for c in range(COLORS)]

# Rugs: 3 rugs, each represented by a list of color membership booleans
rug = [[Bool(f"rug_{r}_{c}") for c in range(COLORS)] for r in range(3)]

# Solid variables: whether each rug is solid
solid = [Bool(f"solid_{r}") for r in range(3)]

# Base solver
solver = Solver()

# Exactly 5 colors used
solver.add(Sum([If(use[c], 1, 0) for c in range(COLORS)]) == 5)

# Each used color appears in exactly one rug
for c in range(COLORS):
    solver.add(use[c] == Or([rug[r][c] for r in range(3)]))
    # If used, appears in exactly one rug
    for r1 in range(3):
        for r2 in range(r1 + 1, 3):
            solver.add(Implies(use[c], Not(And(rug[r1][c], rug[r2][c]))))

# Rugs are disjoint (no color appears in multiple rugs)
for c in range(COLORS):
    for r1 in range(3):
        for r2 in range(r1 + 1, 3):
            solver.add(Not(And(rug[r1][c], rug[r2][c])))

# Exactly two solid rugs
solver.add(Sum([If(solid[r], 1, 0) for r in range(3)]) == 2)

# Solid rug size constraints
for r in range(3):
    # If solid, exactly one color
    solver.add(Implies(solid[r], Sum([If(rug[r][c], 1, 0) for c in range(COLORS)]) == 1))
    # If not solid, at least two colors
    solver.add(Implies(Not(solid[r]), Sum([If(rug[r][c], 1, 0) for c in range(COLORS)]) >= 2))

# Rule constraints per rug
for r in range(3):
    # If white is used, exactly two other colors are also used (total 3 colors)
    solver.add(Implies(rug[r][4], Sum([If(rug[r][c], 1, 0) for c in range(COLORS)]) == 3))
    
    # If olive is used, peach must be used
    solver.add(Implies(rug[r][1], rug[r][2]))
    
    # Forest and turquoise not together
    solver.add(Not(And(rug[r][0], rug[r][3])))
    
    # Peach and turquoise not together
    solver.add(Not(And(rug[r][2], rug[r][3])))
    
    # Peach and yellow not together
    solver.add(Not(And(rug[r][2], rug[r][5])))

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
for idx, (c1, c2) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Try all assignments of the two colors to solid rugs
    found_sat = False
    for r1 in range(3):
        for r2 in range(3):
            if r1 == r2:
                continue
            # Create fresh solver for this assignment
            s_try = Solver()
            s_try.add(s_chk.assertions())
            
            # Make rugs r1 and r2 solid with colors c1 and c2 respectively
            s_try.add(solid[r1])
            s_try.add(solid[r2])
            
            # Ensure rug r1 has exactly color c1
            for c in range(COLORS):
                if c == c1:
                    s_try.add(rug[r1][c])
                else:
                    s_try.add(Not(rug[r1][c]))
            
            # Ensure rug r2 has exactly color c2
            for c in range(COLORS):
                if c == c2:
                    s_try.add(rug[r2][c])
                else:
                    s_try.add(Not(rug[r2][c]))
            
            # Ensure rug r1 and r2 are solid (already enforced by solid[r1], solid[r2])
            # The third rug will automatically get the remaining colors
            
            if s_try.check() == sat:
                found_sat = True
                break
        
        if found_sat:
            break
    
    # If no assignment is SAT, then this pair of solid rugs is impossible
    if not found_sat:
        answer_index_list.append(idx)

print(answer_index_list)