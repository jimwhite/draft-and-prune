from z3 import *

# Band indices: 0-Uneasy, 1-Vegemite, 2-Wellspring, 3-Xpert, 4-Yardsign, 5-Zircon
bands = ["Uneasy", "Vegemite", "Wellspring", "Xpert", "Yardsign", "Zircon"]

# Slot variables: slot[i] = position (1-6) for band i
slot = [Int(f"slot_{i}") for i in range(6)]

# Base solver with original constraints
base_solver = Solver()

# Domain: each slot between 1 and 6, all distinct
for i in range(6):
    base_solver.add(slot[i] >= 1, slot[i] <= 6)
base_solver.add(Distinct(*slot))

# Original constraints
# Vegemite before Zircon: slot[1] < slot[5]
base_solver.add(slot[1] < slot[5])

# Wellspring before Xpert and Zircon before Xpert: slot[2] < slot[3], slot[5] < slot[3]
base_solver.add(slot[2] < slot[3])
base_solver.add(slot[5] < slot[3])

# Uneasy in last three slots: slot[0] >= 4
base_solver.add(slot[0] >= 4)

# Yardsign in first three slots: slot[4] <= 3
base_solver.add(slot[4] <= 3)

# Answer choices (as constraints)
choices = [
    # 0: "Only Uneasy can perform in a later slot than Xpert."
    lambda s: s.add(And(*[Implies(slot[i] > slot[3], i == 0) for i in range(6)])),
    
    # 1: "Vegemite performs in an earlier slot than Wellspring, which performs in an earlier slot than Zircon."
    lambda s: s.add(slot[1] < slot[2], slot[2] < slot[5]),
    
    # 2: "Vegemite and Wellspring each perform in an earlier slot than Xpert."
    lambda s: s.add(slot[1] < slot[3], slot[2] < slot[3]),
    
    # 3: "Xpert performs either immediately before or immediately after Uneasy."
    lambda s: s.add(Or(slot[3] == slot[0] + 1, slot[0] == slot[3] + 1)),
    
    # 4: "Xpert performs in either slot five or slot six."
    lambda s: s.add(Or(slot[3] == 5, slot[3] == 6))
]

# For each choice, check if it's equivalent to the original Wellspring/Zircon-before-Xpert constraint
answer_index_list = []

for idx, choice in enumerate(choices):
    # Clone base solver and remove the original Wellspring/Zircon-before-Xpert constraints
    s_mod = Solver()
    for a in base_solver.assertions():
        if not (a.decl().name() == "and" and 
                len(a.children()) >= 2 and
                any(str(c) == "slot_2 < slot_3" for c in a.children()) and
                any(str(c) == "slot_5 < slot_3" for c in a.children())):
            s_mod.add(a)
    
    # Add the choice constraint
    choice(s_mod)
    
    # Check if this modified set implies the original Wellspring/Zircon-before-Xpert constraints
    # i.e., check if there exists a model where Wellspring >= Xpert OR Zircon >= Xpert
    counter_solver = Solver()
    for a in s_mod.assertions():
        counter_solver.add(a)
    
    # Add negation of original constraint: Wellspring >= Xpert OR Zircon >= Xpert
    counter_solver.add(Or(slot[2] >= slot[3], slot[5] >= slot[3]))
    
    # If UNSAT, then no counterexample exists — the choice preserves the effect
    if counter_solver.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)