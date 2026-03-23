from z3 import *

# Band indices: 0-Uneasy, 1-Vegemite, 2-Wellspring, 3-Xpert, 4-Yardsign, 5-Zircon
bands = ["Uneasy", "Vegemite", "Wellspring", "Xpert", "Yardsign", "Zircon"]
pos = {b: Int(f"pos_{b}") for b in bands}

# Base solver with fixed constraints
base_solver = Solver()

# Domain constraints: positions 1-6, all distinct
for b in bands:
    base_solver.add(pos[b] >= 1, pos[b] <= 6)
base_solver.add(Distinct(*[pos[b] for b in bands]))

# Fixed constraints from problem
base_solver.add(pos["Vegemite"] < pos["Zircon"])  # Vegemite before Zircon
base_solver.add(pos["Uneasy"] >= 4)               # Uneasy in last three slots (4,5,6)
base_solver.add(pos["Yardsign"] <= 3)             # Yardsign in first three slots (1,2,3)

# Original constraint: Wellspring and Zircon before Xpert
original_constraint = And(pos["Wellspring"] < pos["Xpert"], pos["Zircon"] < pos["Xpert"])

# Answer choices as constraints
choice_constraints = [
    # Choice 0: Only Uneasy can perform in a later slot than Xpert
    And(*[pos[b] < pos["Xpert"] for b in bands if b != "Uneasy"]),
    # Choice 1: Vegemite < Wellspring < Zircon
    And(pos["Vegemite"] < pos["Wellspring"], pos["Wellspring"] < pos["Zircon"]),
    # Choice 2: Vegemite and Wellspring before Xpert
    And(pos["Vegemite"] < pos["Xpert"], pos["Wellspring"] < pos["Xpert"]),
    # Choice 3: Xpert immediately before or after Uneasy
    Or(pos["Xpert"] == pos["Uneasy"] + 1, pos["Xpert"] == pos["Uneasy"] - 1),
    # Choice 4: Xpert in slot five or six
    Or(pos["Xpert"] == 5, pos["Xpert"] == 6)
]

# Check equivalence for each choice
answer_index_list = []
for idx, choice_constraint in enumerate(choice_constraints):
    # Solver with original constraint
    s_orig = Solver()
    s_orig.add(base_solver.assertions())
    s_orig.add(original_constraint)
    
    # Solver with choice constraint (replacing original)
    s_choice = Solver()
    s_choice.add(base_solver.assertions())
    s_choice.add(choice_constraint)
    
    # Check if original implies choice (original ∧ ¬choice is UNSAT)
    s_imp1 = Solver()
    s_imp1.add(base_solver.assertions())
    s_imp1.add(original_constraint)
    s_imp1.add(Not(choice_constraint))
    
    # Check if choice implies original (choice ∧ ¬original is UNSAT)
    s_imp2 = Solver()
    s_imp2.add(base_solver.assertions())
    s_imp2.add(choice_constraint)
    s_imp2.add(Not(original_constraint))
    
    # For equivalence, both implications must hold
    if s_imp1.check() == unsat and s_imp2.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)