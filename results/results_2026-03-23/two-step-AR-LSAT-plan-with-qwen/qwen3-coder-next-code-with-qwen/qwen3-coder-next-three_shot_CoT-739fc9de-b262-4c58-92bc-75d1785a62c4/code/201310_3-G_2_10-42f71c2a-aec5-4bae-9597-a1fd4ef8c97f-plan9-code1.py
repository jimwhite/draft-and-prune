from z3 import *

# Employee indices: 0-Myers, 1-Ortega, 2-Paine, 3-Schmidt, 4-Thomson, 5-Wong, 6-Yoder, 7-Zayre
myers, ortega, paine, schmidt, thomson, wong, yoder, zayre = [Bool(f"e_{i}") for i in range(8)]

# Base solver
solver = Solver()

# Global constraint: team size ≥ 4
team_size = Sum([If(v, 1, 0) for v in [myers, ortega, paine, schmidt, thomson, wong, yoder, zayre]])
solver.add(team_size >= 4)

# Conditional constraints
## If Myers is selected, neither Ortega nor Paine can be
solver.add(Implies(myers, Not(ortega)))
solver.add(Implies(myers, Not(paine)))

## If Schmidt is selected, both Paine and Thomson must be
solver.add(Implies(schmidt, paine))
solver.add(Implies(schmidt, thomson))

## If Wong is selected, both Myers and Yoder must be
solver.add(Implies(wong, myers))
solver.add(Implies(wong, yoder))

# Given condition: Yoder is not on the team
solver.add(Not(yoder))

# Answer choices indices: Zayre=7, Thomson=4, Paine=2, Ortega=1, Myers=0
answer_choices = [7, 4, 2, 1, 0]

# Check each answer choice
answer_index_list = []
for idx in answer_choices:
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert this employee is selected
    if idx == 0:
        s_chk.add(myers)
    elif idx == 1:
        s_chk.add(ortega)
    elif idx == 2:
        s_chk.add(paine)
    elif idx == 3:
        s_chk.add(schmidt)
    elif idx == 4:
        s_chk.add(thomson)
    elif idx == 5:
        s_chk.add(wong)
    elif idx == 6:
        s_chk.add(yoder)
    elif idx == 7:
        s_chk.add(zayre)
    
    # If UNSAT, this employee cannot be on the team (EXCEPT answer)
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)