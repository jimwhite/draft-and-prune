from z3 import *

# Color indices: forest=0, olive=1, peach=2, turquoise=3, white=4, yellow=5
colors = ["forest", "olive", "peach", "turquoise", "white", "yellow"]
color_indices = {c: i for i, c in enumerate(colors)}

# Base solver
solver = Solver()

# Exactly 5 colors are used out of 6
used_colors = [Bool(f"used_{c}") for c in colors]
solver.add(Sum([If(uc, 1, 0) for uc in used_colors]) == 5)

# Each color appears in at most one rug
# We'll model rugs as sets of colors using boolean variables: rug[r][c] = True if color c is in rug r
rug = [[Bool(f"rug_{r}_{c}") for c in range(6)] for r in range(3)]

# Constraint: each color used in at most one rug
for c in range(6):
    solver.add(Sum([If(rug[r][c], 1, 0) for r in range(3)]) <= 1)

# Constraint: each color used must be one of the 5 selected colors
for c in range(6):
    for r in range(3):
        solver.add(Implies(rug[r][c], used_colors[c]))

# Exactly two solid rugs, one multicolored rug
solid_rugs = [Bool(f"solid_{r}") for r in range(3)]
solver.add(Sum([If(s, 1, 0) for s in solid_rugs]) == 2)

# Solid rug constraint: size = 1
for r in range(3):
    # If solid, then exactly one color is used in this rug
    solver.add(Implies(solid_rugs[r], Sum([If(rug[r][c], 1, 0) for c in range(6)]) == 1))
    # If not solid (i.e., multicolored), then size >= 2
    solver.add(Implies(Not(solid_rugs[r]), Sum([If(rug[r][c], 1, 0) for c in range(6)]) >= 2))

# Rule: In any rug with white, two other colors are also used (i.e., rug size >= 3 if white present)
for r in range(3):
    solver.add(Implies(rug[r][color_indices["white"]], 
                       Sum([If(rug[r][c], 1, 0) for c in range(6)]) >= 3))

# Rule: If olive is used, peach must also be used (in same rug)
for r in range(3):
    solver.add(Implies(rug[r][color_indices["olive"]], rug[r][color_indices["peach"]]))

# Conflict pairs: forest & turquoise, peach & turquoise, peach & yellow
for r in range(3):
    solver.add(Not(And(rug[r][color_indices["forest"]], rug[r][color_indices["turquoise"]])))
    solver.add(Not(And(rug[r][color_indices["peach"]], rug[r][color_indices["turquoise"]])))
    solver.add(Not(And(rug[r][color_indices["peach"]], rug[r][color_indices["yellow"]])))

# Answer choices: pairs of colors that are the two solid rugs
answer_choices = [
    ("forest", "peach"),
    ("forest", "yellow"),
    ("peach", "turquoise"),
    ("peach", "yellow"),
    ("turquoise", "yellow")
]

# Check each answer choice
answer_index_list = []
for idx, (c1, c2) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Fix the two solid rugs to use exactly these colors
    c1_idx = color_indices[c1]
    c2_idx = color_indices[c2]
    
    # We need to assign these two colors to the two solid rugs
    # There are 3! ways to assign which rug is which, but we can use disjunctions
    # For simplicity: assume rug0 and rug1 are solid, or rug0 and rug2, or rug1 and rug2
    # We'll add all possibilities for which rugs are solid and what colors they have
    
    # First, ensure exactly two rugs are solid (already in solver)
    
    # For each pair of solid rug positions, try to assign the colors
    solid_pairs = [(0, 1), (0, 2), (1, 2)]
    disj = []
    
    for r1, r2 in solid_pairs:
        # Make rugs r1 and r2 solid
        conj = And(solid_rugs[r1], solid_rugs[r2], Not(solid_rugs[3 - r1 - r2]))
        
        # Assign color c1 to rug r1 and c2 to rug r2
        conj = And(conj, rug[r1][c1_idx], rug[r2][c2_idx])
        # Ensure no other colors in these rugs (since solid)
        for c in range(6):
            if c != c1_idx:
                conj = And(conj, Not(rug[r1][c]))
            if c != c2_idx:
                conj = And(conj, Not(rug[r2][c]))
        
        # The remaining colors (5 total used - 2 solid = 3) must go to the multicolored rug
        # Get all used colors: c1, c2, and 3 others from remaining 4 colors
        remaining_colors = [c for c in range(6) if c != c1_idx and c != c2_idx]
        # Exactly 3 of these remaining colors must be used (since total 5 used)
        conj = And(conj, Sum([If(used_colors[c], 1, 0) for c in remaining_colors]) == 3)
        
        # Assign all used colors to the multicolored rug (the one not r1 or r2)
        rm = 3 - r1 - r2
        for c in remaining_colors:
            conj = And(conj, rug[rm][c] == used_colors[c])
        
        disj.append(conj)
    
    s_chk.add(Or(*disj))
    
    # Check if this configuration is possible
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)