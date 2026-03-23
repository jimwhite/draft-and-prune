from z3 import *

# Band indices: Uneasy=0, Vegemite=1, Wellspring=2, Xpert=3, Yardsign=4, Zircon=5
bands = ["Uneasy", "Vegemite", "Wellspring", "Xpert", "Yardsign", "Zircon"]
pos = {b: Int(f"pos_{b}") for b in bands}

# Base solver with original constraints
solver = Solver()

# All-different constraint: positions 1-6, all distinct
positions = [pos[b] for b in bands]
solver.add(Distinct(*positions))
for b in bands:
    solver.add(pos[b] >= 1, pos[b] <= 6)

# Original constraints
solver.add(pos["Vegemite"] < pos["Zircon"])  # Vegemite before Zircon
solver.add(pos["Wellspring"] < pos["Xpert"])  # Wellspring before Xpert
solver.add(pos["Zircon"] < pos["Xpert"])      # Zircon before Xpert
solver.add(pos["Uneasy"] >= 4)                # Uneasy in last three slots (4,5,6)
solver.add(pos["Yardsign"] <= 3)              # Yardsign in first three slots (1,2,3)

# Answer choices as constraints
answer_constraints = [
    # Option A: "Only Uneasy can perform in a later slot than Xpert"
    And(
        pos["Xpert"] < pos["Uneasy"],
        *[pos[b] < pos["Xpert"] for b in bands if b != "Uneasy"]
    ),
    
    # Option B: "Vegemite before Wellspring, which before Zircon"
    And(
        pos["Vegemite"] < pos["Wellspring"],
        pos["Wellspring"] < pos["Zircon"]
    ),
    
    # Option C: "Vegemite and Wellspring each before Xpert"
    And(
        pos["Vegemite"] < pos["Xpert"],
        pos["Wellspring"] < pos["Xpert"]
    ),
    
    # Option D: "Xpert immediately before or after Uneasy"
    Or(
        pos["Xpert"] == pos["Uneasy"] + 1,
        pos["Uneasy"] == pos["Xpert"] + 1
    ),
    
    # Option E: "Xpert in slot five or six"
    Or(pos["Xpert"] == 5, pos["Xpert"] == 6)
]

# Check each answer choice
answer_index_list = []
for idx, constraint in enumerate(answer_constraints):
    # (a) Check compatibility: original constraints + candidate constraint is SAT
    s_compat = Solver()
    s_compat.add(solver.assertions())
    s_compat.add(constraint)
    
    if s_compat.check() == unsat:
        continue  # Not compatible, skip
    
    # (b) Check entailment: in all models of original + candidate, Wellspring and Zircon are before Xpert
    s_entail = Solver()
    s_entail.add(solver.assertions())
    s_entail.add(constraint)
    
    # Negate the target condition: Wellspring >= Xpert OR Zircon >= Xpert
    s_entail.add(Or(pos["Wellspring"] >= pos["Xpert"], pos["Zircon"] >= pos["Xpert"]))
    
    if s_entail.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)