from z3 import *

# Employee indices: Myers=0, Ortega=1, Paine=2, Schmidt=3, Thomson=4, Wong=5, Yoder=6, Zayre=7
m = [Bool(f"m_{i}") for i in range(8)]

# Base solver
solver = Solver()

# Team-size constraint: at least 4 employees selected
solver.add(Sum([If(m[i], 1, 0) for i in range(8)]) >= 4)

# Fixed condition: Yoder is not on the team
solver.add(Not(m[6]))

# Constraint 1: If Myers is selected, neither Ortega nor Paine can be
solver.add(Or(Not(m[0]), Not(m[1]), Not(m[2])))

# Constraint 2: If Schmidt is selected, both Paine and Thomson must be
solver.add(Or(Not(m[3]), m[2], Not(m[4])))
solver.add(Or(Not(m[3]), Not(m[2]), m[4]))
# Alternatively, using implication directly:
# solver.add(Implies(m[3], And(m[2], m[4])))

# Constraint 3: If Wong is selected, both Myers and Yoder must be
# Since Yoder is not on the team (m[6] = False), Wong cannot be selected
solver.add(Not(m[5]))

# Answer choices indices: Zayre=7, Thomson=4, Paine=2, Ortega=1, Myers=0
answer_choices = [7, 4, 2, 1, 0]

# Check each answer choice
answer_index_list = []
for idx, emp_idx in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert this employee is selected
    s_chk.add(m[emp_idx])
    
    # If UNSAT, this employee cannot be on the team (EXCEPT answer)
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)