from z3 import *

# Employee indices
(MYERS, ORTEGA, PAINE, SCHMIDT, THOMSON, WONG, YODER, ZAYRE) = range(8)

# Boolean variables for team selection
emp = [Bool(f"emp_{i}") for i in range(8)]

# Base solver
solver = Solver()

# Team-size constraint: at least 4 employees selected
solver.add(Sum([If(emp[i], 1, 0) for i in range(8)]) >= 4)

# Conditional constraints
## If Myers is selected, neither Ortega nor Paine can be
solver.add(Implies(emp[MYERS], And(Not(emp[ORTEGA]), Not(emp[PAINE]))))

## If Schmidt is selected, both Paine and Thomson must be
solver.add(Implies(emp[SCHMIDT], And(emp[PAINE], emp[THOMSON])))

## If Wong is selected, both Myers and Yoder must be
solver.add(Implies(emp[WONG], And(emp[MYERS], emp[YODER])))

# Yoder exclusion constraint
solver.add(Not(emp[YODER]))

# Answer choices: ['Zayre', 'Thomson', 'Paine', 'Ortega', 'Myers']
answer_choices = [ZAYRE, THOMSON, PAINE, ORTEGA, MYERS]

# Check each answer choice
answer_index_list = []
for idx, emp_idx in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert this candidate employee is selected
    s_chk.add(emp[emp_idx])
    
    # If UNSAT, this employee cannot be on the team when Yoder is excluded
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)