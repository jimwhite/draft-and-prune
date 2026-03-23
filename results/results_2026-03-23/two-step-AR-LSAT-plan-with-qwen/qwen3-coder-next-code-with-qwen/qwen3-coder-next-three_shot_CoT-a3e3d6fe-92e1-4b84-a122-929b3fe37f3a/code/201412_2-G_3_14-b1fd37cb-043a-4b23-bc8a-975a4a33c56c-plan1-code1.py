from z3 import *

# Color indices: forest=0, olive=1, peach=2, turquoise=3, white=4, yellow=5
colors = ["forest", "olive", "peach", "turquoise", "white", "yellow"]
num_colors = 6
num_rugs = 3

# Decision variables
used = [Bool(f"used_{c}") for c in range(num_colors)]
in_rug = [[Bool(f"in_rug_{r}_{c}") for c in range(num_colors)] for r in range(num_rugs)]
solid = [Bool(f"solid_{r}") for r in range(num_rugs)]

# Base solver
solver = Solver()

# Exactly five colors are used
solver.add(Sum([If(used[c], 1, 0) for c in range(num_colors)]) == 5)

# Each used color appears in exactly one rug
for c in range(num_colors):
    solver.add(Implies(used[c], Sum([in_rug[r][c] for r in range(num_rugs)]) == 1))

# Each rug has at least one color
for r in range(num_rugs):
    solver.add(Or([in_rug[r][c] for c in range(num_colors)]))

# Count colors per rug
count = [Int(f"count_{r}") for r in range(num_rugs)]
for r in range(num_rugs):
    solver.add(count[r] == Sum([If(in_rug[r][c], 1, 0) for c in range(num_colors)]))

# Solid rug constraint: count[r] == 1 iff solid[r]
for r in range(num_rugs):
    solver.add(Implies(solid[r], count[r] == 1))
    solver.add(Implies(count[r] == 1, solid[r]))

# Exactly two solid rugs
solver.add(Sum([If(solid[r], 1, 0) for r in range(num_rugs)]) == 2)

# Color compatibility rules per rug
for r in range(num_rugs):
    # If white is used, exactly two other colors must also be used (total 3)
    solver.add(Implies(in_rug[r][4], count[r] == 3))
    
    # If olive is used, peach must also be used
    solver.add(Implies(in_rug[r][1], in_rug[r][2]))
    
    # Forest and turquoise cannot co-occur
    solver.add(Not(And(in_rug[r][0], in_rug[r][3])))
    
    # Peach and turquoise cannot co-occur
    solver.add(Not(And(in_rug[r][2], in_rug[r][3])))
    
    # Peach and yellow cannot co-occur
    solver.add(Not(And(in_rug[r][2], in_rug[r][5])))

# Answer choices: pairs of colors that cannot be the two solid rugs
answer_choices = [
    (0, 2),  # forest and peach
    (0, 5),  # forest and yellow
    (2, 3),  # peach and turquoise
    (2, 5),  # peach and yellow
    (3, 5)   # turquoise and yellow
]

# Check each answer choice
forbidden_pairs = []
for idx, (c1, c2) in enumerate(answer_choices):
    is_forbidden = True
    
    # Try all assignments of the two solid rugs to positions
    for r1 in range(num_rugs):
        for r2 in range(num_rugs):
            if r1 == r2:
                continue
            
            s_chk = Solver()
            s_chk.add(solver.assertions())
            
            # Rug r1 is solid with color c1
            s_chk.add(solid[r1])
            s_chk.add(in_rug[r1][c1] == True)
            
            # Rug r2 is solid with color c2
            s_chk.add(solid[r2])
            s_chk.add(in_rug[r2][c2] == True)
            
            # Other rugs are not solid (must be multicolored, i.e., count >= 2)
            for r in range(num_rugs):
                if r != r1 and r != r2:
                    s_chk.add(count[r] >= 2)
            
            # Ensure colors c1 and c2 are used
            s_chk.add(used[c1])
            s_chk.add(used[c2])
            
            # Ensure c1 and c2 are only in their respective rugs
            for r in range(num_rugs):
                if r != r1:
                    s_chk.add(Not(in_rug[r][c1]))
                if r != r2:
                    s_chk.add(Not(in_rug[r][c2]))
            
            if s_chk.check() == sat:
                is_forbidden = False
                break
        
        if not is_forbidden:
            break
    
    if is_forbidden:
        forbidden_pairs.append(idx)

print(forbidden_pairs)