from z3 import *

# Color indices: forest=0, olive=1, peach=2, turquoise=3, white=4, yellow=5
COLORS = 6
RUGS = 3

# used[c] indicates if color c is used (exactly 5 colors total)
used = [Bool(f"used_{c}") for c in range(COLORS)]

# in_rug[r][c] indicates if color c is used in rug r
in_rug = [[Bool(f"in_rug_{r}_{c}") for c in range(COLORS)] for r in range(RUGS)]

# Base solver
solver = Solver()

# Exactly 5 colors are used
solver.add(Sum([If(used[c], 1, 0) for c in range(COLORS)]) == 5)

# Color usage constraint: used[c] iff color appears in exactly one rug
for c in range(COLORS):
    solver.add(used[c] == Or([in_rug[r][c] for r in range(RUGS)]))

# Solid/multicolored constraint: exactly two solid rugs (one color each), one multicolored rug
# For each rug, count how many colors it uses
rug_size = [Int(f"rug_{r}_size") for r in range(RUGS)]
for r in range(RUGS):
    solver.add(rug_size[r] == Sum([If(in_rug[r][c], 1, 0) for c in range(COLORS)]))

# Exactly two rugs have size == 1, one rug has size >= 2
solid_count = Sum([If(rug_size[r] == 1, 1, 0) for r in range(RUGS)])
solver.add(solid_count == 2)

# Rule constraints per rug
for r in range(RUGS):
    # R1: If white is used, then rug has exactly 3 colors (white + 2 others)
    solver.add(Implies(in_rug[r][4], rug_size[r] == 3))
    
    # R2: If olive is used, then peach is also used
    solver.add(Implies(in_rug[r][1], in_rug[r][2]))
    
    # R3: Forest and turquoise cannot co-occur
    solver.add(Not(And(in_rug[r][0], in_rug[r][3])))
    
    # R4: Peach and turquoise cannot co-occur
    solver.add(Not(And(in_rug[r][2], in_rug[r][3])))
    
    # R5: Peach and yellow cannot co-occur
    solver.add(Not(And(in_rug[r][2], in_rug[r][5])))

# Answer choices: pairs of colors that cannot be the two solid rugs
answer_choices = [
    (0, 2),  # forest and peach
    (0, 5),  # forest and yellow
    (2, 3),  # peach and turquoise
    (2, 5),  # peach and yellow
    (3, 5)   # turquoise and yellow
]

answer_index_list = []

for idx, (color1, color2) in enumerate(answer_choices):
    # Try both assignments: rug0=color1 & rug1=color2, or rug0=color2 & rug1=color1
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assignment 1: rug0 has color1, rug1 has color2
    for c in range(COLORS):
        s_chk.add(in_rug[0][c] == (c == color1))
        s_chk.add(in_rug[1][c] == (c == color2))
    
    # Ensure rug0 and rug1 are solid (size=1) - already enforced by above
    # Ensure rug2 is multicolored (>=2 colors)
    s_chk.add(rug_size[2] >= 2)
    
    # Check first assignment
    res1 = s_chk.check()
    
    if res1 == unsat:
        # Try second assignment: rug0 has color2, rug1 has color1
        s_chk2 = Solver()
        s_chk2.add(solver.assertions())
        
        for c in range(COLORS):
            s_chk2.add(in_rug[0][c] == (c == color2))
            s_chk2.add(in_rug[1][c] == (c == color1))
        
        s_chk2.add(rug_size[2] >= 2)
        
        res2 = s_chk2.check()
        
        if res2 == unsat:
            # Both assignments impossible
            answer_index_list.append(idx)
    # If either assignment is SAT, then this pair is possible (not added to answer_index_list)

print(answer_index_list)