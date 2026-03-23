from z3 import *

# Band indices: Uneasy=0, Vegemite=1, Wellspring=2, Xpert=3, Yardsign=4, Zircon=5
bands = ["Uneasy", "Vegemite", "Wellspring", "Xpert", "Yardsign", "Zircon"]

# Position variables: pos[i] = slot number (1-6) for band i
pos = [Int(f"pos_{i}") for i in range(6)]

# Base solver with original constraints
solver = Solver()

# Domain constraints: positions 1-6
for i in range(6):
    solver.add(pos[i] >= 1, pos[i] <= 6)

# Distinctness constraint
solver.add(Distinct(pos))

# Original constraints
solver.add(pos[1] < pos[5])  # Vegemite before Zircon
solver.add(pos[2] < pos[3], pos[5] < pos[3])  # Wellspring and Zircon before Xpert
solver.add(pos[0] >= 4)  # Uneasy in last three slots (4,5,6)
solver.add(pos[4] <= 3)  # Yardsign in first three slots (1,2,3)

# Original condition: Wellspring and Zircon before Xpert
original_cond = And(pos[2] < pos[3], pos[5] < pos[3])

# Candidate conditions
candidates = [
    # 0: "Only Uneasy can perform in a later slot than Xpert."
    # This means: for all bands except Uneasy, they perform before Xpert
    And(pos[1] < pos[3], pos[2] < pos[3], pos[4] < pos[3], pos[5] < pos[3]),
    
    # 1: "Vegemite performs in an earlier slot than Wellspring, which performs in an earlier slot than Zircon."
    And(pos[1] < pos[2], pos[2] < pos[5]),
    
    # 2: "Vegemite and Wellspring each perform in an earlier slot than Xpert."
    And(pos[1] < pos[3], pos[2] < pos[3]),
    
    # 3: "Xpert performs either immediately before or immediately after Uneasy."
    Or(pos[3] == pos[0] + 1, pos[0] == pos[3] + 1),
    
    # 4: "Xpert performs in either slot five or slot six."
    Or(pos[3] == 5, pos[3] == 6)
]

answer_index_list = []

for idx, cand in enumerate(candidates):
    # Check direction 1: candidate ⇒ original (under other constraints)
    s1 = Solver()
    s1.add(solver.assertions())
    s1.add(cand, Not(original_cond))
    
    # Check direction 2: original ⇒ candidate (under other constraints)
    s2 = Solver()
    s2.add(solver.assertions())
    s2.add(original_cond, Not(cand))
    
    # If both implications hold (both UNSAT), then candidate is equivalent
    if s1.check() == unsat and s2.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)