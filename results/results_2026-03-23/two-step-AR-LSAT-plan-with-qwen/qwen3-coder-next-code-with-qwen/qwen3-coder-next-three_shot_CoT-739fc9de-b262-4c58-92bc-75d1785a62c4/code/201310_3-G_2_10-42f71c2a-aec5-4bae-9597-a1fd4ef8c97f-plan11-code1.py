from z3 import *

# Employee indices: 0-Myers, 1-Ortega, 2-Paine, 3-Schmidt, 4-Thomson, 5-Wong, 6-Yoder, 7-Zayre
m = [Bool(f"m_{i}") for i in range(8)]

# Base solver
solver = Solver()

# Team-size constraint: at least 4 employees
solver.add(Sum([If(m[i], 1, 0) for i in range(8)]) >= 4)

# Fixed constraint: Yoder is not on the team
solver.add(Not(m[6]))

# Conditional constraints:
# If Myers is selected, neither Ortega nor Paine can be
solver.add(Implies(m[0], And(Not(m[1]), Not(m[2]))))

# If Schmidt is selected, both Paine and Thomson must be
solver.add(Implies(m[3], And(m[2], m[4])))

# If Wong is selected, both Myers and Yoder must be
# Since Yoder is excluded (m[6] == False), Wong cannot be selected
solver.add(Implies(m[5], m[6]))
# This effectively forces Wong to be False when Yoder is excluded

# Answer choices: ['Zayre', 'Thomson', 'Paine', 'Ortega', 'Myers']
# Indices: [7, 4, 2, 1, 0]
answer_choices = [7, 4, 2, 1, 0]

# Check each answer choice
answer_index_list = []
for idx in answer_choices:
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert this employee is on the team
    s_chk.add(m[idx])
    
    # If UNSAT, this employee cannot be on the team when Yoder is excluded
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)