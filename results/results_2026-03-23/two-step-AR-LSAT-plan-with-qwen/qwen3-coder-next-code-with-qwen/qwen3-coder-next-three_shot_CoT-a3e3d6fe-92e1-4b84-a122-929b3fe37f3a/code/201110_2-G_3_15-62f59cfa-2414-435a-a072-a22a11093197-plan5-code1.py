from z3 import *

# Rider indices: 0-Reynaldo, 1-Seamus, 2-Theresa, 3-Yuki
# Bicycle indices: 0-F, 1-G, 2-H, 3-J

# Day 1 assignments: d1[r][b] = True if rider r tests bicycle b on day 1
d1 = [[Bool(f"d1_{r}_{b}") for b in range(4)] for r in range(4)]

# Day 2 assignments: d2[r][b] = True if rider r tests bicycle b on day 2
d2 = [[Bool(f"d2_{r}_{b}") for b in range(4)] for r in range(4)]

# Base solver
solver = Solver()

# Day 1 constraints: each rider tests exactly one bicycle, each bicycle tested by exactly one rider
for r in range(4):
    solver.add(PbAtMost([(d1[r][b], 1) for b in range(4)], 1))
    solver.add(PbAtLeast([(d1[r][b], 1) for b in range(4)], 1))
for b in range(4):
    solver.add(PbAtMost([(d1[r][b], 1) for r in range(4)], 1))
    solver.add(PbAtLeast([(d1[r][b], 1) for r in range(4)], 1))

# Day 2 constraints: each rider tests exactly one bicycle, each bicycle tested by exactly one rider
for r in range(4):
    solver.add(PbAtMost([(d2[r][b], 1) for b in range(4)], 1))
    solver.add(PbAtLeast([(d2[r][b], 1) for b in range(4)], 1))
for b in range(4):
    solver.add(PbAtMost([(d2[r][b], 1) for r in range(4)], 1))
    solver.add(PbAtLeast([(d2[r][b], 1) for r in range(4)], 1))

# Global constraints
# Reynaldo cannot test F on either day (Reynaldo=0, F=0)
solver.add(Not(d1[0][0]))
solver.add(Not(d2[0][0]))

# Yuki cannot test J on either day (Yuki=3, J=3)
solver.add(Not(d1[3][3]))
solver.add(Not(d2[3][3]))

# Theresa must test H on at least one day (Theresa=2, H=2)
solver.add(Or(d1[2][2], d2[2][2]))

# The bicycle Yuki tests on day 1 must be tested by Seamus on day 2
for b in range(4):
    solver.add(Implies(d1[3][b], d2[1][b]))

# Answer choices
answer_choices = [
    ("Reynaldo tests J on the first day.", d1[0][3]),      # A
    ("Reynaldo tests J on the second day.", d2[0][3]),     # B
    ("Seamus tests H on the first day.", d1[1][2]),        # C
    ("Yuki tests H on the first day.", d1[3][2]),          # D
    ("Yuki tests H on the second day.", d2[3][2])          # E
]

# Check each answer choice
answer_index_list = []
for idx, (desc, condition) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add the condition for this choice
    s_chk.add(condition)
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)