from z3 import *

# Variables
color_in_rug = Array('color_in_rug', IntSort(), IntSort())
color_used = [Bool('color_used_%d' % i) for i in range(6)]

# Solver
solver = Solver()

# Constraints
solver.add(PbEq([(color_used[i], 1) for i in range(6)], 5))
solver.add(ForAll([c], Implies(color_used[c], And(color_in_rug[c] >= 0, color_in_rug[c] <= 2))))
solver.add(ForAll([c1, c2], Implies(And(c1 != c2, color_used[c1], color_used[c2]), color_in_rug[c1] != color_in_rug[c2])))
solver.add(ForAll([r], Implies(color_in_rug[4] == r, PbEq([(color_in_rug[c] == r, 1) for c in range(6)], 3))))
solver.add(ForAll([r], Implies(color_in_rug[1] == r, color_in_rug[2] == r)))
solver.add(ForAll([r], Not(And(color_in_rug[0] == r, color_in_rug[3] == r))))
solver.add(ForAll([r], Not(And(color_in_rug[2] == r, color_in_rug[3] == r))))
solver.add(ForAll([r], Not(And(color_in_rug[2] == r, color_in_rug[5] == r))))
solver.add(color_used[5])
solver.add(ForAll([r], Implies(color_in_rug[5] == r, PbEq([(color_in_rug[c] == r, 1) for c in range(6)], 1))))


# Answer choices
options = [
    PbEq([(PbEq([(color_in_rug[c] == r, 1) for c in range(6)], 1), 1) for r in range(3)], 1),
    And(color_used[0], Exists([r], And(color_in_rug[0] == r, PbEq([(color_in_rug[c] == r, 1) for c in range(6)], 1)))),
    Not(color_used[3]),
    Exists([r], And(color_in_rug[0] == r, color_in_rug[1] == r)),
    Exists([r], And(color_in_rug[2] == r, color_in_rug[4] == r))
]

for i, option in enumerate(options):
    solver.push()
    solver.add(option)
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()

