from z3 import *

# Band indices: Uneasy=0, Vegemite=1, Wellspring=2, Xpert=3, Yardsign=4, Zircon=5
pos = [Int(f"pos_{i}") for i in range(6)]

# Base solver
solver = Solver()

# Domain constraints: positions 1-6, all distinct
for i in range(6):
    solver.add(pos[i] >= 1, pos[i] <= 6)
solver.add(Distinct(*pos))

# Original constraints
# Vegemite before Zircon: pos[1] < pos[5]
solver.add(pos[1] < pos[5])
# Wellspring and Zircon before Xpert: pos[2] < pos[3], pos[5] < pos[3]
solver.add(pos[2] < pos[3])
solver.add(pos[5] < pos[3])
# Uneasy in last three slots: pos[0] ∈ {4,5,6}
solver.add(Or(pos[0] == 4, pos[0] == 5, pos[0] == 6))
# Yardsign in first three slots: pos[4] ∈ {1,2,3}
solver.add(Or(pos[4] == 1, pos[4] == 2, pos[4] == 3))

# Answer choices
answer_choices = [
    # 0: Only Uneasy can perform in a later slot than Xpert.
    lambda pos: And(*[Implies(pos[i] > pos[3], i == 0) for i in range(6)]),
    # 1: Vegemite < Wellspring < Zircon
    lambda pos: And(pos[1] < pos[2], pos[2] < pos[5]),
    # 2: Vegemite and Wellspring each before Xpert
    lambda pos: And(pos[1] < pos[3], pos[2] < pos[3]),
    # 3: Xpert immediately before or after Uneasy
    lambda pos: Or(pos[3] == pos[0] + 1, pos[0] == pos[3] + 1),
    # 4: Xpert in slot 5 or 6
    lambda pos: Or(pos[3] == 5, pos[3] == 6)
]

answer_index_list = []

for idx, choice_func in enumerate(answer_choices):
    # Clone base solver
    s1 = Solver()
    s1.add(solver.assertions())
    # Add choice constraint
    s1.add(choice_func(pos))
    
    # Check 1: base + choice ⇒ Wellspring < Xpert
    s_check1 = Solver()
    s_check1.add(solver.assertions())
    s_check1.add(choice_func(pos))
    s_check1.add(Not(pos[2] < pos[3]))
    
    # Check 2: base + choice ⇒ Zircon < Xpert
    s_check2 = Solver()
    s_check2.add(solver.assertions())
    s_check2.add(choice_func(pos))
    s_check2.add(Not(pos[5] < pos[3]))
    
    # Check 3: base + original ⇒ choice
    s_check3 = Solver()
    s_check3.add(solver.assertions())
    # Original constraints are already in solver, but we need to assert them explicitly for this check
    s_check3.add(pos[1] < pos[5])
    s_check3.add(pos[2] < pos[3])
    s_check3.add(pos[5] < pos[3])
    # Add negation of choice
    s_check3.add(Not(choice_func(pos)))
    
    if (s_check1.check() == unsat and 
        s_check2.check() == unsat and 
        s_check3.check() == unsat):
        answer_index_list.append(idx)

print(answer_index_list)