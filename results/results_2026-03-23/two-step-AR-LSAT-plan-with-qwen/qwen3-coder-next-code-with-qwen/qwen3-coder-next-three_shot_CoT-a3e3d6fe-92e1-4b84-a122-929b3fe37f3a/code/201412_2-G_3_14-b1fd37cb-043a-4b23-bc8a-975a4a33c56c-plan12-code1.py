from z3 import *

# Color indices: forest=0, olive=1, peach=2, turquoise=3, white=4, yellow=5
colors = ["forest", "olive", "peach", "turquoise", "white", "yellow"]
num_colors = 6
num_rugs = 3

# Boolean variables for whether each color is used at all
color_used = [Bool(f"color_used_{c}") for c in range(num_colors)]

# Boolean variables: rug[i][c] = True if rug i uses color c
rug = [[Bool(f"rug_{i}_{c}") for c in range(num_colors)] for i in range(num_rugs)]

# Base solver
solver = Solver()

# Exactly five colors are used
solver.add(Sum([If(color_used[c], 1, 0) for c in range(num_colors)]) == 5)

# Link color_used to rug usage: color_used[c] iff at least one rug uses color c
for c in range(num_colors):
    solver.add(color_used[c] == Or([rug[i][c] for i in range(num_rugs)]))

# Each color is used in at most one rug
for c in range(num_colors):
    for i in range(num_rugs):
        for j in range(i + 1, num_rugs):
            solver.add(Not(And(rug[i][c], rug[j][c])))

# Exactly two solid rugs (one multicolored rug)
# For each rug, count how many colors it uses
rug_color_counts = [Sum([If(rug[i][c], 1, 0) for c in range(num_colors)]) for i in range(num_rugs)]

# Rule constraints for each rug
for i in range(num_rugs):
    # If white used, at least 3 colors total
    solver.add(Implies(rug[i][4], rug_color_counts[i] >= 3))
    
    # If olive used, peach must be used
    solver.add(Implies(rug[i][1], rug[i][2]))
    
    # Forest and turquoise not together
    solver.add(Not(And(rug[i][0], rug[i][3])))
    
    # Peach and turquoise not together
    solver.add(Not(And(rug[i][2], rug[i][3])))
    
    # Peach and yellow not together
    solver.add(Not(And(rug[i][2], rug[i][5])))

# Answer choices: pairs of colors that cannot be the two solid rugs
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
    
    # Try all possible assignments of the two solid colors to rugs
    found_sat = False
    
    # Try rug0 and rug1 as the solid rugs with colors c1 and c2
    for (r1, r2) in [(0, 1), (0, 2), (1, 2)]:
        s_chk_temp = Solver()
        s_chk_temp.add(solver.assertions())
        
        # Set rug r1 to be solid with color c1
        for c in range(num_colors):
            if c == c1:
                s_chk_temp.add(rug[r1][c])
            else:
                s_chk_temp.add(Not(rug[r1][c]))
        
        # Set rug r2 to be solid with color c2
        for c in range(num_colors):
            if c == c2:
                s_chk_temp.add(rug[r2][c])
            else:
                s_chk_temp.add(Not(rug[r2][c]))
        
        # The remaining rug must be multicolored (>= 2 colors)
        r3 = [i for i in range(num_rugs) if i != r1 and i != r2][0]
        s_chk_temp.add(rug_color_counts[r3] >= 2)
        
        # Ensure exactly two solid rugs: the other two rugs must have count == 1
        s_chk_temp.add(rug_color_counts[r1] == 1)
        s_chk_temp.add(rug_color_counts[r2] == 1)
        
        if s_chk_temp.check() == sat:
            found_sat = True
            break
    
    # If no assignment works, this pair cannot be the two solid rugs
    if not found_sat:
        answer_index_list.append(idx)

print(answer_index_list)