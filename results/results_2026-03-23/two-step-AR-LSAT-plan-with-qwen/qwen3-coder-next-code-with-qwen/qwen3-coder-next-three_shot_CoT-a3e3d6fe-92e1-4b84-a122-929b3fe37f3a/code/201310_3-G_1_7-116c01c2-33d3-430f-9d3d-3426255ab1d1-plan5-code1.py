from z3 import *

# Band indices: Uneasy=0, Vegemite=1, Wellspring=2, Xpert=3, Yardsign=4, Zircon=5
bands = ["Uneasy", "Vegemite", "Wellspring", "Xpert", "Yardsign", "Zircon"]

# Position variables (1-based: slots 1-6)
pos = [Int(f"pos_{i}") for i in range(6)]

# Base solver with original constraints
solver = Solver()

# Domain: positions 1-6, all distinct
for i in range(6):
    solver.add(pos[i] >= 1, pos[i] <= 6)
solver.add(Distinct(*pos))

# Original constraints
# Vegemite < Zircon (Vegemite performs earlier than Zircon)
solver.add(pos[1] < pos[5])
# Wellspring and Zircon each perform earlier than Xpert
solver.add(pos[2] < pos[3])
solver.add(pos[5] < pos[3])
# Uneasy in one of last three slots (slots 4,5,6 → positions >= 4)
solver.add(pos[0] >= 4)
# Yardsign in one of first three slots (slots 1,2,3 → positions <= 3)
solver.add(pos[4] <= 3)

# Answer choices as constraints
answer_constraints = [
    # A: "Only Uneasy can perform in a later slot than Xpert"
    # This means: (1) Uneasy > Xpert, and (2) for all other bands B != 0: B < Xpert
    And(
        pos[0] > pos[3],
        pos[1] < pos[3],
        pos[2] < pos[3],
        pos[4] < pos[3],
        pos[5] < pos[3]
    ),
    
    # B: "Vegemite < Wellspring ∧ Wellspring < Zircon"
    And(pos[1] < pos[2], pos[2] < pos[5]),
    
    # C: "Vegemite and Wellspring each perform earlier than Xpert"
    And(pos[1] < pos[3], pos[2] < pos[3]),
    
    # D: "Xpert performs either immediately before or immediately after Uneasy"
    Or(pos[3] == pos[0] + 1, pos[0] == pos[3] + 1),
    
    # E: "Xpert performs in either slot five or slot six"
    Or(pos[3] == 5, pos[3] == 6)
]

# Check each choice for logical equivalence with original constraint: (Wellspring < Xpert ∧ Zircon < Xpert)
answer_index_list = []

for idx, new_constraint in enumerate(answer_constraints):
    # Check entailment 1: Original constraints ⊨ new constraint
    s1 = Solver()
    s1.add(solver.assertions())
    s1.add(Not(new_constraint))
    entailment1 = (s1.check() == unsat)  # If UNSAT, then new constraint must hold
    
    # Check entailment 2: new constraint + other constraints ⊨ (Wellspring < Xpert ∧ Zircon < Xpert)
    s2 = Solver()
    # Add all original constraints except the two we want to replace
    for assertion in solver.assertions():
        if not (assertion == (pos[2] < pos[3]) or assertion == (pos[5] < pos[3])):
            s2.add(assertion)
    # Add the new constraint
    s2.add(new_constraint)
    # Check if original constraints are implied
    s2.add(Not(And(pos[2] < pos[3], pos[5] < pos[3])))
    entailment2 = (s2.check() == unsat)  # If UNSAT, then original constraint must hold
    
    if entailment1 and entailment2:
        answer_index_list.append(idx)

print(answer_index_list)