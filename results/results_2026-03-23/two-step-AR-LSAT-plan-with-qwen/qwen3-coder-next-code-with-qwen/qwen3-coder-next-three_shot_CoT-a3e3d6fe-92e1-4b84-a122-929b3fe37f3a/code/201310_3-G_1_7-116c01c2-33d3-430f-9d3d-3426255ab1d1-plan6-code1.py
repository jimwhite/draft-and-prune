from z3 import *

# Band indices: Uneasy=0, Vegemite=1, Wellspring=2, Xpert=3, Yardsign=4, Zircon=5
bands = ["Uneasy", "Vegemite", "Wellspring", "Xpert", "Yardsign", "Zircon"]

# Position variables: pos[i] = slot number (1-6) for band i
pos = [Int(f"pos_{i}") for i in range(6)]

# Base solver with original constraints
original_solver = Solver()

# All-different constraint: positions are a permutation of 1..6
original_solver.add(Distinct(*pos))

# Domain constraints: each position between 1 and 6
for i in range(6):
    original_solver.add(pos[i] >= 1, pos[i] <= 6)

# Original constraints:
# Vegemite before Zircon: pos[1] < pos[5]
original_solver.add(pos[1] < pos[5])

# Wellspring and Zircon before Xpert: pos[2] < pos[3], pos[5] < pos[3]
original_solver.add(pos[2] < pos[3])
original_solver.add(pos[5] < pos[3])

# Uneasy in last three slots: pos[0] ∈ {4,5,6}
original_solver.add(Or(pos[0] == 4, pos[0] == 5, pos[0] == 6))

# Yardsign in first three slots: pos[4] ∈ {1,2,3}
original_solver.add(Or(pos[4] == 1, pos[4] == 2, pos[4] == 3))

# Answer choices constraints
def choice_a_constraint():
    # Only Uneasy can perform in a later slot than Xpert:
    # (1) Uneasy is after Xpert: pos[0] > pos[3]
    # (2) All others are before Xpert: for i ≠ 0, pos[i] < pos[3]
    return And(
        pos[0] > pos[3],
        pos[1] < pos[3],
        pos[2] < pos[3],
        pos[4] < pos[3],
        pos[5] < pos[3]
    )

def choice_b_constraint():
    # Vegemite < Wellspring < Zircon: pos[1] < pos[2] < pos[5]
    return And(pos[1] < pos[2], pos[2] < pos[5])

def choice_c_constraint():
    # Vegemite and Wellspring each before Xpert: pos[1] < pos[3], pos[2] < pos[3]
    return And(pos[1] < pos[3], pos[2] < pos[3])

def choice_d_constraint():
    # Xpert immediately before or after Uneasy: |pos[3] - pos[0]| = 1
    return Or(pos[3] == pos[0] + 1, pos[0] == pos[3] + 1)

def choice_e_constraint():
    # Xpert in slot 5 or 6: pos[3] ∈ {5,6}
    return Or(pos[3] == 5, pos[3] == 6)

# Check logical equivalence for each choice
answer_index_list = []

for idx, (choice_name, constraint_func) in enumerate([
    ("A", choice_a_constraint),
    ("B", choice_b_constraint),
    ("C", choice_c_constraint),
    ("D", choice_d_constraint),
    ("E", choice_e_constraint)
]):
    # Check 1: original_solver + NOT(choice) should be UNSAT (choice is necessary)
    s1 = Solver()
    s1.add(original_solver.assertions())
    s1.add(Not(constraint_func()))
    
    # Check 2: choice_solver + NOT(original) should be UNSAT (choice is sufficient)
    s2 = Solver()
    # Add only the choice constraint
    s2.add(constraint_func())
    
    # Add original constraints except "Wellspring and Zircon before Xpert"
    s2.add(pos[1] < pos[5])  # Vegemite before Zircon
    s2.add(Or(pos[0] == 4, pos[0] == 5, pos[0] == 6))  # Uneasy in last three
    s2.add(Or(pos[4] == 1, pos[4] == 2, pos[4] == 3))  # Yardsign in first three
    s2.add(Distinct(*pos))
    for i in range(6):
        s2.add(pos[i] >= 1, pos[i] <= 6)
    
    # Add NOT of original "Wellspring and Zircon before Xpert"
    s2.add(Not(And(pos[2] < pos[3], pos[5] < pos[3])))
    
    # If both s1 and s2 are UNSAT, then the choice is logically equivalent
    if s1.check() == unsat and s2.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)