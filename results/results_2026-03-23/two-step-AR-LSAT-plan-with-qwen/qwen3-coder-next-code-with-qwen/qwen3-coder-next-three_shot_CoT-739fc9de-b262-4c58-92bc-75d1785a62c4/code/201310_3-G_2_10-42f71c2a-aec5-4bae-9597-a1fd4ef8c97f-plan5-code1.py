from z3 import *

# Employee indices: Myers=0, Ortega=1, Paine=2, Schmidt=3, Thomson=4, Wong=5, Yoder=6, Zayre=7
M, O, P, S, T, W, Y, Z = Bools(['Myers', 'Ortega', 'Paine', 'Schmidt', 'Thomson', 'Wong', 'Yoder', 'Zayre'])

# Base solver
solver = Solver()

# Fixed constraint: Yoder is not selected
solver.add(Not(Y))

# Minimum team size constraint: at least 4 employees
team_size = Sum([If(m, 1, 0) for m in [M, O, P, S, T, W, Y, Z]])
solver.add(team_size >= 4)

# Implication constraints
# If Myers is selected, neither Ortega nor Paine can be
solver.add(Implies(M, And(Not(O), Not(P))))

# If Schmidt is selected, both Paine and Thomson must be
solver.add(Implies(S, And(P, T)))

# If Wong is selected, both Myers and Yoder must be
solver.add(Implies(W, And(M, Y)))

# Since Y is false, Wong cannot be selected (W => M and Y, but Y is false)
solver.add(Not(W))

# Answer choices: Zayre=7, Thomson=4, Paine=2, Ortega=1, Myers=0
answer_choices = ['Zayre', 'Thomson', 'Paine', 'Ortega', 'Myers']
employee_vars = [Z, T, P, O, M]

# Check each answer choice
answer_index_list = []
for idx, emp_var in enumerate(employee_vars):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert the candidate employee is selected
    s_chk.add(emp_var)
    
    # If UNSAT, this employee cannot be on the team (EXCEPT answer)
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)