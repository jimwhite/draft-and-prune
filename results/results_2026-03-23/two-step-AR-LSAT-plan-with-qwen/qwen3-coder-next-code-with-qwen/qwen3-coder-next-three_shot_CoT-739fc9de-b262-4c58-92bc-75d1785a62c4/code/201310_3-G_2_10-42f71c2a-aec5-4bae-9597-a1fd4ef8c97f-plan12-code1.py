from z3 import *

# Employee indices: Myers=0, Ortega=1, Paine=2, Schmidt=3, Thomson=4, Wong=5, Yoder=6, Zayre=7
t = [Bool(f"t_{i}") for i in range(8)]

# Base solver
solver = Solver()

# Team size constraint: at least 4 employees
solver.add(Sum([If(t[i], 1, 0) for i in range(8)]) >= 4)

# Yoder not on team (given)
solver.add(t[6] == False)

# Myers constraint: If Myers is selected, neither Ortega nor Paine can be
solver.add(Or(Not(t[0]), And(Not(t[1]), Not(t[2]))))

# Schmidt constraint: If Schmidt is selected, both Paine and Thomson must be
solver.add(Or(Not(t[3]), And(t[2], t[4])))

# Wong constraint: If Wong is selected, both Myers and Yoder must be
# Since Yoder is not on team (t[6] == False), Wong cannot be selected
solver.add(t[5] == False)

# Answer choices indices: Zayre=7, Thomson=4, Paine=2, Ortega=1, Myers=0
answer_choices = [7, 4, 2, 1, 0]

# Check each answer choice
forbidden_list = []
for idx in answer_choices:
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraint that this candidate is on the team
    s_chk.add(t[idx] == True)
    
    # If UNSAT, this candidate cannot be on the team
    if s_chk.check() == unsat:
        forbidden_list.append(idx)

print(forbidden_list)