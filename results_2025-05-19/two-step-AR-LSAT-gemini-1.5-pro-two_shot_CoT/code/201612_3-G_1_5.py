from z3 import *

# Define variables
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

# Constraint 6 (Team Sizes - adjusted for Mei's assignment)
solver.add(PbEq([(team_assignment[s] == 0, 1) for s in range(5)], 3))


# Constraint 7 (One facilitator per team)
solver.add(PbEq([(And(team_assignment[s] == 0, facilitator[s]), 1) for s in range(5)], 1))
solver.add(PbEq([(And(team_assignment[s] == 1, facilitator[s]), 1) for s in range(5)], 1))

# Constraint 8 (Mei on Green)
solver.add(team_assignment[3] == 0)

# Answer choices
choices = [
    team_assignment[0] == 0,  # A
    team_assignment[1] == 1,  # B
    team_assignment[4] == 0,  # C
    facilitator[2],          # D
    facilitator[3]           # E
]

for i in range(len(choices)):
    solver.push()
    solver.add(choices[i])
    if solver.check() == sat:
        solver.push()
        solver.add(Not(choices[i]))
        if solver.check() == unsat:
            print(f"Option {chr(65 + i)} is correct")
            exit()
        solver.pop()
    solver.pop()