from z3 import *

# Variables
team_assignment = Array('team_assignment', IntSort(), IntSort())
facilitator = Array('facilitator', IntSort(), BoolSort())

solver = Solver()

# Constraints 1-5
for s in range(5):
    solver.add(Or(team_assignment[s] == 0, team_assignment[s] == 1))
solver.add(team_assignment[0] != team_assignment[4])
solver.add(team_assignment[2] == 0)
solver.add(Not(facilitator[1]))
solver.add(facilitator[4])

# Constraint 6 (Team Sizes)
count_green = Sum([If(team_assignment[s] == 0, 1, 0) for s in range(5)])
count_red = Sum([If(team_assignment[s] == 1, 1, 0) for s in range(5)])
solver.add(Or(And(count_green == 3, count_red == 2), And(count_green == 2, count_red == 3)))

# Constraint 7 (One Facilitator per Team)
fac_green = Sum([If(And(team_assignment[s] == 0, facilitator[s]), 1, 0) for s in range(5)])
fac_red = Sum([If(And(team_assignment[s] == 1, facilitator[s]), 1, 0) for s in range(5)])
solver.add(And(fac_green == 1, fac_red == 1))

# Check answer choices
negations = [
    team_assignment[0] == 0,  # A
    Not(facilitator[2]),  # B
    team_assignment[4] == 1,  # C
    And(facilitator[0], facilitator[3]),  # D
    Or(facilitator[0], facilitator[1])  # E
]

for i in range(len(negations)):
    solver.push()
    solver.add(negations[i])
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()