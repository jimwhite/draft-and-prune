from z3 import *

# Band indices: Uneasy=0, Vegemite=1, Wellspring=2, Xpert=3, Yardsign=4, Zircon=5
bands = ["Uneasy", "Vegemite", "Wellspring", "Xpert", "Yardsign", "Zircon"]
pos = {b: Int(f"pos_{b}") for b in bands}

# Base solver with original constraints
solver = Solver()

# Domain constraints: positions 1-6
for b in bands:
    solver.add(pos[b] >= 1, pos[b] <= 6)

# All-different constraint
solver.add(Distinct(*[pos[b] for b in bands]))

# Original constraints from problem
solver.add(pos["Vegemite"] < pos["Zircon"])  # Vegemite before Zircon
solver.add(pos["Wellspring"] < pos["Xpert"]) # Wellspring before Xpert
solver.add(pos["Zircon"] < pos["Xpert"])     # Zircon before Xpert
solver.add(pos["Uneasy"] >= 4)               # Uneasy in last three slots (4,5,6)
solver.add(pos["Yardsign"] <= 3)             # Yardsign in first three slots (1,2,3)

# Answer choices as constraints
answer_constraints = [
    # A: Only Uneasy can perform in a later slot than Xpert.
    # This means: For all bands b != Uneasy, pos[b] < pos[Xpert]
    # i.e., Vegemite, Wellspring, Yardsign, Zircon all before Xpert
    And(
        pos["Vegemite"] < pos["Xpert"],
        pos["Wellspring"] < pos["Xpert"],
        pos["Yardsign"] < pos["Xpert"],
        pos["Zircon"] < pos["Xpert"]
    ),
    
    # B: Vegemite before Wellspring, which before Zircon
    And(
        pos["Vegemite"] < pos["Wellspring"],
        pos["Wellspring"] < pos["Zircon"]
    ),
    
    # C: Vegemite and Wellspring each before Xpert
    And(
        pos["Vegemite"] < pos["Xpert"],
        pos["Wellspring"] < pos["Xpert"]
    ),
    
    # D: Xpert immediately before or after Uneasy
    Or(
        pos["Xpert"] == pos["Uneasy"] + 1,
        pos["Uneasy"] == pos["Xpert"] + 1
    ),
    
    # E: Xpert in slot five or six
    Or(pos["Xpert"] == 5, pos["Xpert"] == 6)
]

# Function to check logical equivalence
def is_equivalent(candidate_constraint):
    # Clone base solver with original constraints
    s1 = Solver()
    s1.add(solver.assertions())
    
    # Add candidate constraint
    s1.add(candidate_constraint)
    
    # Check (i) New => Original: Add negation of original constraint and check UNSAT
    # Original constraint we want to replicate: Wellspring < Xpert AND Zircon < Xpert
    original_constraint = And(pos["Wellspring"] < pos["Xpert"], pos["Zircon"] < pos["Xpert"])
    s1_check_i = Solver()
    s1_check_i.add(s1.assertions())
    s1_check_i.add(Not(original_constraint))
    
    # If SAT, new does not imply original
    if s1_check_i.check() == sat:
        return False
    
    # Check (ii) Original => New: Add original constraint and negation of new, check UNSAT
    s1_check_ii = Solver()
    s1_check_ii.add(solver.assertions())
    s1_check_ii.add(original_constraint, Not(candidate_constraint))
    
    # If SAT, original does not imply new
    if s1_check_ii.check() == sat:
        return False
    
    return True

# Check each answer choice
answer_index_list = []
for idx, constraint in enumerate(answer_constraints):
    if is_equivalent(constraint):
        answer_index_list.append(idx)

# Print the index of the correct choice (should be exactly one)
print(answer_index_list[0] if answer_index_list else -1)