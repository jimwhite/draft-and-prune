from z3 import *

# Employee indices: Myers=0, Ortega=1, Paine=2, Schmidt=3, Thomson=4, Wong=5, Yoder=6, Zayre=7
myers, ortega, paine, schmidt, thomson, wong, yoder, zayre = [Bool(f) for f in ['myers', 'orteaga', 'paine', 'schmidt', 'thomson', 'wong', 'yoder', 'zayre']]

# Base solver
solver = Solver()

# Yoder is not on the team
solver.add(Not(yoder))

# At-least-four constraint
team_size = Sum([If(v, 1, 0) for v in [myers, ortega, paine, schmidt, thomson, wong, yoder, zayre]])
solver.add(team_size >= 4)

# Conditional constraints
## If Myers is on the team, neither Ortega nor Paine can be
solver.add(Implies(myers, And(Not(ortega), Not(paine))))

## If Schmidt is on the team, both Paine and Thomson must also be
solver.add(Implies(schmidt, And(paine, thomson)))

## If Wong is on the team, both Myers and Yoder must also be
solver.add(Implies(wong, And(myers, yoder)))

# Since Yoder is False, Wong's constraint simplifies to: wong → false ⇒ ¬wong
solver.add(Not(wong))

# Answer choices (in order): Zayre=7, Thomson=4, Paine=2, Ortega=1, Myers=0
answer_choices = [
    zayre,
    thomson,
    paine,
    ortega,
    myers
]

# Check each answer choice: find which one CANNOT be on the team when Yoder is absent
impossible_candidates = []
for idx, emp in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assume this candidate is on the team
    s_chk.add(emp)
    
    if s_chk.check() == unsat:
        impossible_candidates.append(idx)

# Print the index of the first (and only) impossible candidate
print(impossible_candidates[0] if impossible_candidates else -1)