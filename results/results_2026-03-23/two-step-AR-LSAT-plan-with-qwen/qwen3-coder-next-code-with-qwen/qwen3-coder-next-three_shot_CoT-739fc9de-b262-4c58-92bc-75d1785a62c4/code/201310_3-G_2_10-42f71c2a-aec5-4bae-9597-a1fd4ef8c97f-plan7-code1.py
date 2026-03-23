from z3 import *

# Employee indices: Myers=0, Ortega=1, Paine=2, Schmidt=3, Thomson=4, Wong=5, Yoder=6, Zayre=7
t = [Bool(f"t_{i}") for i in range(8)]

# Base solver
solver = Solver()

# Team-size constraint: at least 4 employees
solver.add(Sum([If(t[i], 1, 0) for i in range(8)]) >= 4)

# Conditional constraints
# If Myers is selected, neither Ortega nor Paine can be
solver.add(Implies(t[0], And(Not(t[1]), Not(t[2]))))

# If Schmidt is selected, both Paine and Thomson must be
solver.add(Implies(t[3], And(t[2], t[4])))

# If Wong is selected, both Myers and Yoder must be
solver.add(Implies(t[5], And(t[0], t[6])))

# Given condition: Yoder is not on the team
solver.add(Not(t[6]))

# Answer choices (in order): Zayre=7, Thomson=4, Paine=2, Ortega=1, Myers=0
answer_choices = [7, 4, 2, 1, 0]

# Check each answer choice
answer_index_list = []
for idx, emp_idx in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert this candidate is selected
    s_chk.add(t[emp_idx])
    
    # If UNSAT, this candidate cannot be on the team (EXCEPT answer)
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)