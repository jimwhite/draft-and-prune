from z3 import *

# Employee indices: Myers=0, Ortega=1, Paine=2, Schmidt=3, Thomson=4, Wong=5, Yoder=6, Zayre=7
team = [Bool(f"team_{i}") for i in range(8)]

# Base solver
solver = Solver()

# Minimum-size constraint: at least 4 employees
solver.add(Sum([If(t, 1, 0) for t in team]) >= 4)

# Conditional constraints
# If Myers is selected, neither Ortega nor Paine can be: team[0] → (¬team[1] ∧ ¬team[2])
solver.add(Implies(team[0], And(Not(team[1]), Not(team[2]))))

# If Schmidt is selected, both Paine and Thomson must be: team[3] → (team[2] ∧ team[4])
solver.add(Implies(team[3], And(team[2], team[4])))

# If Wong is selected, both Myers and Yoder must be: team[5] → (team[0] ∧ team[6])
solver.add(Implies(team[5], And(team[0], team[6])))

# Yoder exclusion constraint (as per question condition)
solver.add(Not(team[6]))

# Answer choices: Zayre=7, Thomson=4, Paine=2, Ortega=1, Myers=0
answer_choices = [7, 4, 2, 1, 0]

# Check each answer choice
answer_index_list = []
for idx in answer_choices:
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert this employee is selected
    s_chk.add(team[idx])
    
    # If UNSAT, this employee cannot be on the team (EXCEPT answer)
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)