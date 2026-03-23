from z3 import *

# Color indices: forest=0, olive=1, peach=2, turquoise=3, white=4, yellow=5
COLORS = 6
RUGS = 3

# used[c] indicates if color c is used (exactly 5 colors total)
used = [Bool(f"used_{c}") for c in range(COLORS)]

# in_rug[r][c] indicates if color c is used in rug r
in_rug = [[Bool(f"in_rug_{r}_{c}") for c in range(COLORS)] for r in range(RUGS)]

solver = Solver()

# Exactly 5 colors are used
solver.add(Sum([If(used[c], 1, 0) for c in range(COLORS)]) == 5)

# Each used color appears in exactly one rug
for c in range(COLORS):
    solver.add(Implies(used[c], Sum([If(in_rug[r][c], 1, 0) for r in range(RUGS)]) == 1))
    solver.add(Implies(Not(used[c]), And([Not(in_rug[r][c]) for r in range(RUGS)])))

# Exactly two rugs are solid (exactly one color per rug)
solid_count = 0
for r in range(RUGS):
    # Count colors in rug r
    count_colors = Sum([If(in_rug[r][c], 1, 0) for c in range(COLORS)])
    # Rug r is solid iff count_colors == 1
    solver.add(Implies(count_colors == 1, And([in_rug[r][c] for c in range(COLORS) if c != 0 or True])))
    solver.add(Implies(count_colors == 1, Or([in_rug[r][c] for c in range(COLORS)])))
    # We'll handle solid count separately by adding constraint later

# Instead, directly enforce exactly two rugs are solid:
# For each rug r, define is_solid[r] as (exactly one color in the rug)
is_solid = [Bool(f"is_solid_{r}") for r in range(RUGS)]
for r in range(RUGS):
    # is_solid[r] iff exactly one color is used in rug r
    count_colors = Sum([If(in_rug[r][c], 1, 0) for c in range(COLORS)])
    solver.add(is_solid[r] == (count_colors == 1))

solver.add(Sum([If(is_solid[r], 1, 0) for r in range(RUGS)]) == 2)

# Rule constraints:
# White rule: If white is in rug r, then at least two other colors are also used in that rug
for r in range(RUGS):
    white_in_rug = in_rug[r][4]
    other_colors_count = Sum([If(in_rug[r][c], 1, 0) for c in range(COLORS) if c != 4])
    solver.add(Implies(white_in_rug, other_colors_count >= 3))

# Olive ⇒ peach in same rug
for r in range(RUGS):
    solver.add(Implies(in_rug[r][1], in_rug[r][2]))

# Forest and turquoise conflict
for r in range(RUGS):
    solver.add(Not(And(in_rug[r][0], in_rug[r][3])))

# Peach and turquoise conflict
for r in range(RUGS):
    solver.add(Not(And(in_rug[r][2], in_rug[r][3])))

# Peach and yellow conflict
for r in range(RUGS):
    solver.add(Not(And(in_rug[r][2], in_rug[r][5])))

# Answer choices: pairs of colors that are the solid rugs
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
    
    # Assume rug 0 is solid with color c1, rug 1 is solid with color c2
    # (We can fix which rugs are solid without loss of generality due to symmetry)
    for r in range(RUGS):
        if r == 0:
            # Rug 0 is solid with color c1
            solver_for_rug = Solver()
            for cc in range(COLORS):
                if cc == c1:
                    s_chk.add(in_rug[0][cc])
                else:
                    s_chk.add(Not(in_rug[0][cc]))
            s_chk.add(is_solid[0])
        elif r == 1:
            # Rug 1 is solid with color c2
            for cc in range(COLORS):
                if cc == c2:
                    s_chk.add(in_rug[1][cc])
                else:
                    s_chk.add(Not(in_rug[1][cc]))
            s_chk.add(is_solid[1])
        else:
            # Rug 2 is multicolored (not solid)
            s_chk.add(Not(is_solid[2]))
    
    # Ensure colors c1 and c2 are used (they appear in rugs)
    s_chk.add(used[c1])
    s_chk.add(used[c2])
    
    # Ensure no other rug uses c1 or c2
    for r in range(2, RUGS):
        s_chk.add(Not(in_rug[r][c1]))
        s_chk.add(Not(in_rug[r][c2]))
    for r in [0, 1]:
        # Already handled above
        pass
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)