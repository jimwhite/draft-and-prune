from z3 import *

# Color indices: forest=0, olive=1, peach=2, turquoise=3, white=4, yellow=5
colors = ["forest", "olive", "peach", "turquoise", "white", "yellow"]
num_colors = 6
num_rugs = 3

# Boolean variables: used[c] indicates if color c is used
used = [Bool(f"used_{c}") for c in range(num_colors)]

# Boolean variables: c_in_r[c][r] indicates if color c is used in rug r
c_in_r = [[Bool(f"c_{c}_in_r{r}") for r in range(num_rugs)] for c in range(num_colors)]

# Base solver
solver = Solver()

# Exactly five colors are used
solver.add(Sum([If(used[c], 1, 0) for c in range(num_colors)]) == 5)

# Usage constraint: if used[c] is true, then it appears in exactly one rug
for c in range(num_colors):
    # If used[c], then sum of c_in_r[c][r] over rugs = 1
    solver.add(Implies(used[c], Sum([If(c_in_r[c][r], 1, 0) for r in range(num_rugs)]) == 1))
    # If not used[c], then c_in_r[c][r] = false for all rugs
    solver.add(Implies(Not(used[c]), And([Not(c_in_r[c][r]) for r in range(num_rugs)])))

# Exactly two rugs are solid
solid_count = 0
for r in range(num_rugs):
    # Count colors in rug r
    colors_in_rug = [If(c_in_r[c][r], 1, 0) for c in range(num_colors)]
    # For solid rug: exactly one color used
    is_solid = And([Or(Not(c_in_r[c][r]) for c in range(num_colors) if c != target_c) for target_c in range(num_colors)])
    # Instead, use a more direct approach: rug r is solid iff exactly one color_in_r[c][r] is true
    # We'll handle this by adding constraints for each rug to be solid or not

# Instead, use a different approach: exactly two rugs have exactly one color
rug_solid = [Bool(f"rug_{r}_solid") for r in range(num_rugs)]
for r in range(num_rugs):
    # rug_solid[r] is true iff exactly one color is used in rug r
    count_colors = Sum([If(c_in_r[c][r], 1, 0) for c in range(num_colors)])
    solver.add(Implies(rug_solid[r], count_colors == 1))
    solver.add(Implies(Not(rug_solid[r]), count_colors >= 2))

# Exactly two rugs are solid
solver.add(Sum([If(rug_solid[r], 1, 0) for r in range(num_rugs)]) == 2)

# Rule constraints per rug
for r in range(num_rugs):
    # White rule: if white is used, then at least two other colors are also used
    solver.add(Implies(c_in_r[4][r], Sum([If(c_in_r[c][r], 1, 0) for c in range(num_colors) if c != 4]) >= 2))
    
    # Olive → Peach: if olive is used, then peach must be used
    solver.add(Implies(c_in_r[1][r], c_in_r[2][r]))
    
    # Forest and turquoise not together
    solver.add(Not(And(c_in_r[0][r], c_in_r[3][r])))
    
    # Peach and turquoise not together
    solver.add(Not(And(c_in_r[2][r], c_in_r[3][r])))
    
    # Peach and yellow not together
    solver.add(Not(And(c_in_r[2][r], c_in_r[5][r])))

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
    
    # Add constraints for the two solid rugs to be c1 and c2
    # Assume rug0 is solid with color c1, rug1 is solid with color c2
    # (We need to consider all permutations, but since rugs are indistinct in ordering,
    #  we can fix which rug is which for simplicity)
    
    # For rug0: only color c1 is used
    s_chk.add(c_in_r[c1][0])
    for c in range(num_colors):
        if c != c1:
            s_chk.add(Not(c_in_r[c][0]))
    s_chk.add(rug_solid[0])
    
    # For rug1: only color c2 is used
    s_chk.add(c_in_r[c2][1])
    for c in range(num_colors):
        if c != c2:
            s_chk.add(Not(c_in_r[c][1]))
    s_chk.add(rug_solid[1])
    
    # For rug2: at least two colors used (multicolored)
    s_chk.add(Not(rug_solid[2]))
    
    # Ensure exactly five colors are used
    # Colors c1 and c2 are used, so we need 3 more colors from the remaining 4
    # But we don't need to explicitly add this since the solver will handle it
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)