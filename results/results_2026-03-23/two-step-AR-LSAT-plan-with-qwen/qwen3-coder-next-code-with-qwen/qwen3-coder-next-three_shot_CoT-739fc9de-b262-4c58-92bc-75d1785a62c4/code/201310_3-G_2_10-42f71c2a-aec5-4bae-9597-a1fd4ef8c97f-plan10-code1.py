from z3 import *

# Employee indices: Myers=0, Ortega=1, Paine=2, Schmidt=3, Thomson=4, Wong=5, Yoder=6, Zayre=7
myers, ortega, paine, schmidt, thomson, wong, yoder, zayre = [Bool(f"{name}") for name in
    ["myers", "ortega", "paine", "schmidt", "thomson", "wong", "yoder", "zayre"]]

# Base solver
solver = Solver()

# At-least-four constraint
solver.add(Sum([If(name, 1, 0) for name in [myers, ortega, paine, schmidt, thomson, wong, yoder, zayre]]) >= 4)

# Yoder not selected
solver.add(Not(yoder))

# Conditional constraints:
# If Myers is selected, neither Ortega nor Paine can be: myers ⇒ (¬ortega ∧ ¬paine)
solver.add(Or(Not(myers), Not(ortega)))
solver.add(Or(Not(myers), Not(paine)))

# If Schmidt is selected, both Paine and Thomson must be: schmidt ⇒ (paine ∧ thomson)
solver.add(Or(Not(schmidt), paine))
solver.add(Or(Not(schmidt), thomson))

# If Wong is selected, both Myers and Yoder must be: wong ⇒ (myers ∧ yoder)
# Since yoder is False, this becomes: wong ⇒ (myers ∧ False) ≡ ¬wong
solver.add(Not(wong))

# Answer choices: Zayre=7, Thomson=4, Paine=2, Ortega=1, Myers=0
answer_choices = [
    zayre,
    thomson,
    paine,
    ortega,
    myers
]

# Check each answer choice
answer_index_list = []
for idx, candidate in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert candidate is selected
    s_chk.add(candidate)
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)