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

# Given constraints
base_solver.add(pos["Vegemite"] < pos["Zircon"])
base_solver.add(pos["Wellspring"] < pos["Xpert"], pos["Zircon"] < pos["Xpert"])
base_solver.add(pos["Uneasy"] >= 4)
base_solver.add(pos["Yardsign"] <= 3)

# Answer choices
choices = [
    # A: Only Uneasy can perform in a later slot than Xpert
    lambda p: And(
        p["Xpert"] < p["Uneasy"],
        p["Vegemite"] < p["Xpert"],
        p["Wellspring"] < p["Xpert"],
        p["Yardsign"] < p["Xpert"],
        p["Zircon"] < p["Xpert"]
    ),
    # B: Vegemite before Wellspring, Wellspring before Zircon
    lambda p: And(p["Vegemite"] < p["Wellspring"], p["Wellspring"] < p["Zircon"]),
    # C: Vegemite and Wellspring each before Xpert
    lambda p: And(p["Vegemite"] < p["Xpert"], p["Wellspring"] < p["Xpert"]),
    # D: Xpert immediately before or after Uneasy
    lambda p: Abs(p["Xpert"] - p["Uneasy"]) == 1,
    # E: Xpert in slot five or six
    lambda p: Or(p["Xpert"] == 5, p["Xpert"] == 6)
]

answer_index_list = []

for idx, cond_func in enumerate(choices):
    # Clone base solver
    s1 = Solver()
    s1.add(base_solver.assertions())
    
    # Add new condition
    s1.add(cond_func(pos))
    
    # Check 1: New condition must imply original Wellspring < Xpert and Zircon < Xpert
    # i.e., if we assume ¬(Wellspring < Xpert ∨ Zircon < Xpert), it should be UNSAT
    s1_check1 = Solver()
    s1_check1.add(base_solver.assertions())
    s1_check1.add(cond_func(pos))
    s1_check1.add(Or(pos["Wellspring"] >= pos["Xpert"], pos["Zircon"] >= pos["Xpert"]))
    
    # Check 2: Original constraints must imply new condition under other fixed constraints
    # i.e., if we assume original constraints + other fixed + ¬new condition, it should be UNSAT
    s1_check2 = Solver()
    s1_check2.add(base_solver.assertions())
    s1_check2.add(Not(cond_func(pos)))
    
    # If either check is SAT, the new condition doesn't replace the original
    if s1_check1.check() == sat or s1_check2.check() == sat:
        continue
    
    # Additional check: ensure the new condition + other constraints is SAT
    if s1.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)