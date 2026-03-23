from z3 import *

# Color indices: forest=0, olive=1, peach=2, turquoise=3, white=4, yellow=5
COLORS = 6
forest, olive, peach, turquoise, white, yellow = range(COLORS)

# Create Boolean variables for each rug and color
rug = [[Bool(f"rug_{r}_{c}") for c in range(COLORS)] for r in range(3)]

# Base solver
solver = Solver()

# Exactly five colors are used (exactly one excluded)
used = [Bool(f"used_{c}") for c in range(COLORS)]
solver.add(Sum([If(used[c], 1, 0) for c in range(COLORS)]) == 5)

# Each used color appears in exactly one rug
for c in range(COLORS):
    # If used[c] is true, then exactly one rug uses color c
    solver.add(Implies(used[c], Sum([If(rug[r][c], 1, 0) for r in range(3)]) == 1))
    # If used[c] is false, then no rug uses color c
    solver.add(Implies(Not(used[c]), And([Not(rug[r][c]) for r in range(3)])))

# Each rug is either solid (1 color) or multicolored (>=2 colors)
# Exactly two rugs are solid, one is multicolored
rug_sizes = [Sum([If(rug[r][c], 1, 0) for c in range(COLORS)]) for r in range(3)]
# Exactly two rugs have size 1, one rug has size >=2
solver.add(Or(
    And(rug_sizes[0] == 1, rug_sizes[1] == 1, rug_sizes[2] >= 2),
    And(rug_sizes[0] == 1, rug_sizes[2] == 1, rug_sizes[1] >= 2),
    And(rug_sizes[1] == 1, rug_sizes[2] == 1, rug_sizes[0] >= 2)
))

# Rule constraints for each rug
for r in range(3):
    # R1: If white is used, then exactly two other colors are also used
    solver.add(Implies(rug[r][white], Sum([If(rug[r][c], 1, 0) for c in range(COLORS) if c != white]) == 2))
    
    # R2: If olive is used, then peach is also used
    solver.add(Implies(rug[r][olive], rug[r][peach]))
    
    # R3: Forest and turquoise not together
    solver.add(Not(And(rug[r][forest], rug[r][turquoise])))
    
    # R4: Peach and turquoise not together
    solver.add(Not(And(rug[r][peach], rug[r][turquoise])))
    
    # R5: Peach and yellow not together
    solver.add(Not(And(rug[r][peach], rug[r][yellow])))

# Answer choices: pairs of solid rug colors
answer_choices = [
    (forest, peach),      # index 0: "forest and peach"
    (forest, yellow),     # index 1: "forest and yellow"
    (peach, turquoise),   # index 2: "peach and turquoise"
    (peach, yellow),      # index 3: "peach and yellow"
    (turquoise, yellow)   # index 4: "turquoise and yellow"
]

# Check each answer choice
answer_index_list = []
for idx, (c1, c2) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assume rug0 is solid with color c1, rug1 is solid with color c2
    # (We'll try all permutations: rug0/c1 & rug1/c2, rug0/c1 & rug2/c2, rug1/c1 & rug2/c2)
    found_sat = False
    
    # Try all assignments of the two solid colors to different rugs
    for r1 in range(3):
        for r2 in range(3):
            if r1 == r2:
                continue
            
            s_chk.push()
            
            # Set rug[r1] to be solid with color c1
            for c in range(COLORS):
                if c == c1:
                    s_chk.add(rug[r1][c])
                else:
                    s_chk.add(Not(rug[r1][c]))
            
            # Set rug[r2] to be solid with color c2
            for c in range(COLORS):
                if c == c2:
                    s_chk.add(rug[r2][c])
                else:
                    s_chk.add(Not(rug[r2][c]))
            
            # The remaining rug (r3) must be multicolored
            r3 = 3 - r1 - r2  # Since r1 and r2 are distinct, this gives the third index
            s_chk.add(Sum([If(rug[r3][c], 1, 0) for c in range(COLORS)]) >= 2)
            
            if s_chk.check() == sat:
                found_sat = True
                s_chk.pop()
                break
            
            s_chk.pop()
        
        if found_sat:
            break
    
    # If no assignment is satisfiable, then this pair cannot be the two solid rugs
    if not found_sat:
        answer_index_list.append(idx)

print(answer_index_list)