from z3 import *

# Color indices: forest=0, olive=1, peach=2, turquoise=3, white=4, yellow=5
FOREST, OLIVE, PEACH, TURQ, WHITE, YELLOW = range(6)

# Create Boolean variables for color usage
c = [Bool(f"c_{i}") for i in range(6)]

# Create Boolean variables for rug assignments: r[j][i] = True if rug j uses color i
r = [[Bool(f"r_{j}_{i}") for i in range(6)] for j in range(3)]

# Create Boolean variables for whether rug j is solid
is_solid = [Bool(f"is_solid_{j}") for j in range(3)]

# Base solver
solver = Solver()

# Exactly five colors are used
solver.add(Sum([If(c[i], 1, 0) for i in range(6)]) == 5)

# Link color usage to rug assignments
for i in range(6):
    solver.add(c[i] == Or(r[0][i], r[1][i], r[2][i]))

# For each rug, determine if it's solid
for j in range(3):
    # Count colors used in rug j
    count_colors = Sum([If(r[j][i], 1, 0) for i in range(6)])
    # is_solid[j] iff exactly one color is used
    solver.add(is_solid[j] == (count_colors == 1))

# Exactly two solid rugs
solver.add(Sum([If(is_solid[j], 1, 0) for j in range(3)]) == 2)

# Rule constraints per rug
for j in range(3):
    # If white is used, exactly two other colors must also be used (total 3 colors)
    solver.add(Implies(r[j][WHITE], Sum([If(r[j][i], 1, 0) for i in range(6)]) == 3))
    
    # If olive is used, peach must also be used
    solver.add(Implies(r[j][OLIVE], r[j][PEACH]))
    
    # Forest and turquoise cannot co-occur
    solver.add(Not(And(r[j][FOREST], r[j][TURQ])))
    
    # Peach and turquoise cannot co-occur
    solver.add(Not(And(r[j][PEACH], r[j][TURQ])))
    
    # Peach and yellow cannot co-occur
    solver.add(Not(And(r[j][PEACH], r[j][YELLOW])))

# Answer choices: pairs of colors that cannot be the two solid rugs
answer_choices = [
    (FOREST, PEACH),      # 0: forest and peach
    (FOREST, YELLOW),     # 1: forest and yellow
    (PEACH, TURQ),        # 2: peach and turquoise
    (PEACH, YELLOW),      # 3: peach and yellow
    (TURQ, YELLOW)        # 4: turquoise and yellow
]

# Check each answer choice
answer_index_list = []
for idx, (color1, color2) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraint: exactly two rugs are solid
    s_chk.add(Sum([If(is_solid[j], 1, 0) for j in range(3)]) == 2)
    
    # One solid rug uses color1, another uses color2
    # We need to assign these colors to two different rugs
    # Create auxiliary variables for rug assignments of the solid colors
    # For simplicity, enumerate all ways to assign color1 and color2 to two different rugs
    
    # Case 1: rug0 uses color1, rug1 uses color2
    case1 = And(
        is_solid[0], is_solid[1],
        r[0][color1], Not(Or([r[0][i] for i in range(6) if i != color1])),
        r[1][color2], Not(Or([r[1][i] for i in range(6) if i != color2]))
    )
    
    # Case 2: rug0 uses color2, rug1 uses color1
    case2 = And(
        is_solid[0], is_solid[1],
        r[0][color2], Not(Or([r[0][i] for i in range(6) if i != color2])),
        r[1][color1], Not(Or([r[1][i] for i in range(6) if i != color1]))
    )
    
    # Case 3: rug0 uses color1, rug2 uses color2
    case3 = And(
        is_solid[0], is_solid[2],
        r[0][color1], Not(Or([r[0][i] for i in range(6) if i != color1])),
        r[2][color2], Not(Or([r[2][i] for i in range(6) if i != color2]))
    )
    
    # Case 4: rug0 uses color2, rug2 uses color1
    case4 = And(
        is_solid[0], is_solid[2],
        r[0][color2], Not(Or([r[0][i] for i in range(6) if i != color2])),
        r[2][color1], Not(Or([r[2][i] for i in range(6) if i != color1]))
    )
    
    # Case 5: rug1 uses color1, rug2 uses color2
    case5 = And(
        is_solid[1], is_solid[2],
        r[1][color1], Not(Or([r[1][i] for i in range(6) if i != color1])),
        r[2][color2], Not(Or([r[2][i] for i in range(6) if i != color2]))
    )
    
    # Case 6: rug1 uses color2, rug2 uses color1
    case6 = And(
        is_solid[1], is_solid[2],
        r[1][color2], Not(Or([r[1][i] for i in range(6) if i != color2])),
        r[2][color1], Not(Or([r[2][i] for i in range(6) if i != color1]))
    )
    
    # Add disjunction of all cases
    s_chk.add(Or(case1, case2, case3, case4, case5, case6))
    
    # If UNSAT, this pair cannot be the solid rugs
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)