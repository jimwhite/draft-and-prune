from z3 import *

# Band indices: Uneasy=0, Vegemite=1, Wellspring=2, Xpert=3, Yardsign=4, Zircon=5
bands = ["Uneasy", "Vegemite", "Wellspring", "Xpert", "Yardsign", "Zircon"]
pos = [Int(f"pos_{i}") for i in range(6)]

# Base solver with original constraints
solver = Solver()

# Distinctness constraint
solver.add(Distinct(pos))

# Original constraints
solver.add(pos[1] < pos[5])  # Vegemite before Zircon
solver.add(pos[2] < pos[3], pos[5] < pos[3])  # Wellspring and Zircon before Xpert
solver.add(pos[0] >= 4)  # Uneasy in last three slots (positions 4,5,6)
solver.add(pos[4] <= 3)  # Yardsign in first three slots (positions 1,2,3)

# Answer choices as constraints
answer_choices = [
    # "Only Uneasy can perform in a later slot than Xpert."
    lambda: And(*[Implies(pos[i] > pos[3], i == 0) for i in range(6)]),
    # "Vegemite performs in an earlier slot than Wellspring, which performs in an earlier slot than Zircon."
    lambda: And(pos[1] < pos[2], pos[2] < pos[5]),
    # "Vegemite and Wellspring each perform in an earlier slot than Xpert."
    lambda: And(pos[1] < pos[3], pos[2] < pos[3]),
    # "Xpert performs either immediately before or immediately after Uneasy."
    lambda: Or(pos[3] == pos[0] + 1, pos[0] == pos[3] + 1),
    # "Xpert performs in either slot five or slot six."
    lambda: Or(pos[3] == 5, pos[3] == 6)
]

# Check each choice for logical equivalence with original Wellspring/Zircon-before-Xpert constraint
answer_index_list = []
for idx, choice in enumerate(answer_choices):
    # Clone base solver
    s1 = Solver()
    s1.add(solver.assertions())
    
    # Add the candidate constraint instead of original Wellspring/Zircon-before-Xpert
    s1.add(choice())
    
    # Check if candidate implies original constraint (original must hold in all models of candidate)
    s_imp1 = Solver()
    s_imp1.add(s1.assertions())
    # Add negation of original Wellspring/Zircon-before-Xpert: (Wellspring >= Xpert) OR (Zircon >= Xpert)
    s_imp1.add(Or(pos[2] >= pos[3], pos[5] >= pos[3]))
    impl1 = s_imp1.check() == unsat
    
    # Check if original implies candidate (candidate must hold in all models of original)
    s_imp2 = Solver()
    s_imp2.add(solver.assertions())
    # Add negation of candidate constraint
    if idx == 0:
        s_imp2.add(Not(And(*[Implies(pos[i] > pos[3], i == 0) for i in range(6)])))
    elif idx == 1:
        s_imp2.add(Not(And(pos[1] < pos[2], pos[2] < pos[5])))
    elif idx == 2:
        s_imp2.add(Not(And(pos[1] < pos[3], pos[2] < pos[3])))
    elif idx == 3:
        s_imp2.add(Not(Or(pos[3] == pos[0] + 1, pos[0] == pos[3] + 1)))
    elif idx == 4:
        s_imp2.add(Not(Or(pos[3] == 5, pos[3] == 6)))
    
    impl2 = s_imp2.check() == unsat
    
    if impl1 and impl2:
        answer_index_list.append(idx)

print(answer_index_list)