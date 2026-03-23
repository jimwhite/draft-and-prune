from z3 import *

# Employee indices: Myers, Ortega, Paine, Schmidt, Thomson, Wong, Yoder, Zayre
(MYERS, ORTEGA, PAINE, SCHMIDT, THOMSON, WONG, YODER, ZAYRE) = range(8)

# Boolean variables for each employee
employees = [Bool(f"e_{i}") for i in range(8)]

# Base solver
solver = Solver()

# Minimum size constraint: at least 4 employees selected
solver.add(Sum([If(employees[i], 1, 0) for i in range(8)]) >= 4)

# Conditional constraints
# If Myers is selected, neither Ortega nor Paine can be
solver.add(Or(Not(employees[MYERS]), Not(employees[ORTEGA])))
solver.add(Or(Not(employees[MYERS]), Not(employees[PAINE])))

# If Schmidt is selected, both Paine and Thomson must be
solver.add(Or(Not(employees[SCHMIDT]), employees[PAINE]))
solver.add(Or(Not(employees[SCHMIDT]), employees[THOMSON]))

# If Wong is selected, both Myers and Yoder must be
solver.add(Or(Not(employees[WONG]), employees[MYERS]))
solver.add(Or(Not(employees[WONG]), employees[YODER]))

# Given assumption: Yoder is not on the team
solver.add(Not(employees[YODER]))

# Answer choices
answer_choices = [
    ZAYRE,
    THOMSON,
    PAINE,
    ORTEGA,
    MYERS
]

# Check each answer choice
forbidden_index_list = []
for idx, emp_idx in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert this candidate is selected
    s_chk.add(employees[emp_idx])
    
    # If UNSAT, this employee cannot be on the team when Yoder is excluded
    if s_chk.check() == unsat:
        forbidden_index_list.append(idx)

print(forbidden_index_list)