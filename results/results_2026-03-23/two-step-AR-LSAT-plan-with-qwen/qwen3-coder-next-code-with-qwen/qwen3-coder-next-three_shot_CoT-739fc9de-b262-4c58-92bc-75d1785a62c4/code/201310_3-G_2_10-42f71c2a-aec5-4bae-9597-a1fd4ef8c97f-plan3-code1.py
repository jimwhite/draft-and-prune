from z3 import *

# Employee indices
(MYERS, ORTEGA, PAINE, SCHMIDT, THOMSON, WONG, YODER, ZAYRE) = range(8)

# Boolean variables for selection
m = [Bool(f"m_{i}") for i in range(8)]

# Base solver
solver = Solver()

# Minimum size constraint: at least 4 employees
solver.add(Sum([If(m[i], 1, 0) for i in range(8)]) >= 4)

# Myers constraint: if Myers is selected, neither Ortega nor Paine can be
solver.add(Implies(m[MYERS], And(Not(m[ORTEGA]), Not(m[PAINE]))))

# Schmidt constraint: if Schmidt is selected, both Paine and Thomson must be
solver.add(Implies(m[SCHMIDT], And(m[PAINE], m[THOMSON])))

# Wong constraint: if Wong is selected, both Myers and Yoder must be
solver.add(Implies(m[WONG], And(m[MYERS], m[YODER])))

# Given condition: Yoder is not on the team
solver.add(Not(m[YODER]))

# Answer choices
answer_choices = [
    ZAYRE,
    THOMSON,
    PAINE,
    ORTEGA,
    MYERS
]

# Check each answer choice to find who cannot be on the team
forbidden_list = []
for idx, emp in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert this employee is selected
    s_chk.add(m[emp])
    
    # If UNSAT, this employee cannot be on the team
    if s_chk.check() == unsat:
        forbidden_list.append(idx)

print(forbidden_list)