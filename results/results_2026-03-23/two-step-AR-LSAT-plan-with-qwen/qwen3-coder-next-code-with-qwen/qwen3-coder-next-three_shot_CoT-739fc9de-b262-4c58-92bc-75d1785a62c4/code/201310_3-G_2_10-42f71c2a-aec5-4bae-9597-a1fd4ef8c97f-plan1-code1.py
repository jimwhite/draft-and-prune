from z3 import *

# Employee indices: Myers, Ortega, Paine, Schmidt, Thomson, Wong, Yoder, Zayre
(MYERS, ORTEGA, PAINE, SCHMIDT, THOMSON, WONG, YODER, ZAYRE) = range(8)

# Boolean variables for each employee
employees = [Bool(f"e_{i}") for i in range(8)]

# Base solver
solver = Solver()

# Minimum team size constraint: at least 4 employees
solver.add(Sum([If(employees[i], 1, 0) for i in range(8)]) >= 4)

# Myers constraint: if Myers is selected, neither Ortega nor Paine can be
solver.add(Implies(employees[MYERS], And(Not(employees[ORTEGA]), Not(employees[PAINE]))))

# Schmidt constraint: if Schmidt is selected, both Paine and Thomson must be
solver.add(Implies(employees[SCHMIDT], And(employees[PAINE], employees[THOMSON])))

# Wong constraint: if Wong is selected, both Myers and Yoder must be
solver.add(Implies(employees[WONG], And(employees[MYERS], employees[YODER])))

# Yoder is not on the team
solver.add(Not(employees[YODER]))

# Answer choices
answer_choices = [
    ZAYRE,
    THOMSON,
    PAINE,
    ORTEGA,
    MYERS
]

# Check each answer choice to find which one CANNOT be on the team when Yoder is excluded
forced_exclusion_list = []
for idx, emp_idx in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert this candidate is selected
    s_chk.add(employees[emp_idx])
    
    # If UNSAT, this employee cannot be on the team when Yoder is excluded
    if s_chk.check() == unsat:
        forced_exclusion_list.append(idx)

print(forced_exclusion_list)