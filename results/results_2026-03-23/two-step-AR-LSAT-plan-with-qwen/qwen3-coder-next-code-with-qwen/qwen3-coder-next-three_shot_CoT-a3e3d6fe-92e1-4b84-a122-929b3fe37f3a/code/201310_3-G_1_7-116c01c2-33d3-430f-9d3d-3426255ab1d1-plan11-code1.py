from z3 import *

# Band indices: 0-Uneasy, 1-Vegemite, 2-Wellspring, 3-Xpert, 4-Yardsign, 5-Zircon
bands = ["Uneasy", "Vegemite", "Wellspring", "Xpert", "Yardsign", "Zircon"]

# Position variables: pos[i] = slot position (1-6) for band i
pos = [Int(f"pos_{i}") for i in range(6)]

# Base solver with original constraints
solver_orig = Solver()

# Domain constraints: positions 1-6, all distinct
for i in range(6):
    solver_orig.add(pos[i] >= 1, pos[i] <= 6)
solver_orig.add(Distinct(*pos))

# Original constraints
# Vegemite before Zircon: pos[1] < pos[5]
solver_orig.add(pos[1] < pos[5])

# Wellspring and Zircon each before Xpert: pos[2] < pos[3] and pos[5] < pos[3]
solver_orig.add(pos[2] < pos[3])
solver_orig.add(pos[5] < pos[3])

# Uneasy in last three slots: pos[0] ∈ {4,5,6}
solver_orig.add(Or(pos[0] == 4, pos[0] == 5, pos[0] == 6))

# Yardsign in first three slots: pos[4] ∈ {1,2,3}
solver_orig.add(Or(pos[4] == 1, pos[4] == 2, pos[4] == 3))

# Answer choices as constraints
answer_choices = [
    # A: Only Uneasy can perform in a later slot than Xpert
    # => pos[3] < pos[0] AND for all other bands B (B != 0), pos[B] < pos[3]
    And(pos[3] < pos[0], 
        pos[1] < pos[3], pos[2] < pos[3], pos[4] < pos[3], pos[5] < pos[3]),
    
    # B: Vegemite before Wellspring, which before Zircon
    And(pos[1] < pos[2], pos[2] < pos[5]),
    
    # C: Vegemite and Wellspring each before Xpert
    And(pos[1] < pos[3], pos[2] < pos[3]),
    
    # D: Xpert immediately before or after Uneasy
    Or(pos[3] == pos[0] + 1, pos[0] == pos[3] + 1),
    
    # E: Xpert in slot five or six
    Or(pos[3] == 5, pos[3] == 6)
]

answer_index_list = []

for idx, choice_constraint in enumerate(answer_choices):
    # Solver with original constraints + answer choice
    s1 = Solver()
    s1.add(solver_orig.assertions())
    s1.add(choice_constraint)
    
    # Solver with original constraints but WITHOUT Wellspring/Zircon < Xpert, plus answer choice
    s2 = Solver()
    # Add domain and other original constraints except Wellspring/Zircon < Xpert
    for i in range(6):
        s2.add(pos[i] >= 1, pos[i] <= 6)
    s2.add(Distinct(*pos))
    s2.add(pos[1] < pos[5])  # Vegemite before Zircon
    s2.add(Or(pos[0] == 4, pos[0] == 5, pos[0] == 6))  # Uneasy in last three
    s2.add(Or(pos[4] == 1, pos[4] == 2, pos[4] == 3))  # Yardsign in first three
    s2.add(choice_constraint)
    
    # Check equivalence:
    # 1. Every model of original constraints must satisfy the answer choice (s1 should be SAT if solver_orig is SAT)
    # 2. Every model of s2 must satisfy the original Wellspring/Zircon < Xpert constraints
    
    # Check 1: If solver_orig is SAT, then s1 should be SAT (i.e., answer choice doesn't contradict original)
    # But more importantly: check if original constraints imply the answer choice
    s1_check = Solver()
    s1_check.add(solver_orig.assertions())
    s1_check.add(Not(choice_constraint))
    
    # Check 2: Check if answer choice + other constraints implies original Wellspring/Zircon < Xpert
    s2_check = Solver()
    # Add all constraints of s2 (answer choice + other original except Wellspring/Zircon < Xpert)
    for i in range(6):
        s2_check.add(pos[i] >= 1, pos[i] <= 6)
    s2_check.add(Distinct(*pos))
    s2_check.add(pos[1] < pos[5])
    s2_check.add(Or(pos[0] == 4, pos[0] == 5, pos[0] == 6))
    s2_check.add(Or(pos[4] == 1, pos[4] == 2, pos[4] == 3))
    s2_check.add(choice_constraint)
    # Add negation of original Wellspring/Zircon < Xpert
    s2_check.add(Or(pos[2] >= pos[3], pos[5] >= pos[3]))
    
    # If both checks are UNSAT, then equivalence holds
    if s1_check.check() == unsat and s2_check.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)