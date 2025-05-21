from z3 import *

# Define variables
color_to_rug = Function('color_to_rug', IntSort(), IntSort())
is_color_in_rug = Function('is_color_in_rug', IntSort(), IntSort(), BoolSort())
F, O, P, T, W, Y = 0, 1, 2, 3, 4, 5
RUGS = range(3)
COLORS = range(6)

solver = Solver()

# C0 (Exactly 5 colors used)
solver.add(PbEq([(color_to_rug(c) != -1, 1) for c in COLORS], 5))

# C1 (Used colors assigned to valid rugs)
c = Int('c')
solver.add(ForAll([c], Implies(color_to_rug(c) != -1, Or([color_to_rug(c) == r for r in RUGS]))))

# C2 (Connecting variables)
c = Int('c')
r = Int('r')
solver.add(ForAll([c, r], is_color_in_rug(r, c) == (color_to_rug(c) == r)))

# C3 (White Rule)
r = Int('r')
solver.add(ForAll([r], Implies(is_color_in_rug(r, W), PbEq([(is_color_in_rug(r, c), 1) for c in COLORS if c != W], 2))))

# C4 (Olive Rule)
r = Int('r')
solver.add(ForAll([r], Implies(is_color_in_rug(r, O), is_color_in_rug(r, P))))

# C5 (Forest/Turquoise Rule)
r = Int('r')
solver.add(ForAll([r], Not(And(is_color_in_rug(r, F), is_color_in_rug(r, T)))))

# C6 (Peach/Turquoise Rule)
r = Int('r')
solver.add(ForAll([r], Not(And(is_color_in_rug(r, P), is_color_in_rug(r, T)))))

# C7 (Peach/Yellow Rule)
r = Int('r')
solver.add(ForAll([r], Not(And(is_color_in_rug(r, P), is_color_in_rug(r, Y)))))

# C8 (Question Premise - Forest and Peach together)
r = Int('r')
solver.add(Exists([r], And(is_color_in_rug(r, F), is_color_in_rug(r, P))))

# Check answer choices
answer_choices = [
    PbEq([(PbEq([(is_color_in_rug(r, c), 1) for c in COLORS], 1), 1) for r in RUGS], 1),  # A
    color_to_rug(W) == -1,  # B
    color_to_rug(Y) == -1,  # C
    Exists([r], And(is_color_in_rug(r, T), is_color_in_rug(r, W))),  # D
    Exists([r], And(is_color_in_rug(r, T), is_color_in_rug(r, Y)))   # E
]

for i, choice in enumerate(answer_choices):
    solver.push()
    solver.add(choice)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()