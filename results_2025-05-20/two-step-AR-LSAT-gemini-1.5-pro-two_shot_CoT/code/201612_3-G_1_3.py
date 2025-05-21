from z3 import *

# Define variables
team_assignment = Array('team_assignment', IntSort(), IntSort())
facilitator = Array('facilitator', IntSort(), BoolSort())

solver = Solver()

# Constraint 1: Team Assignment
for s in range(5):
    solver.add(And(team_assignment[s] >= 0, team_assignment[s] <= 1))

# Constraint 2: Team sizes
solver.add(Or(
    And(PbEq([(team_assignment[s] == 0, 1) for s in range(5)], 2),
        PbEq([(team_assignment[s] == 1, 1) for s in range(5)], 3)),
    And(PbEq([(team_assignment[s] == 0, 1) for s in range(5)], 3),
        PbEq([(team_assignment[s] == 1, 1) for s in range(5)], 2))
))

# Constraint 3: Juana and Olga different teams
solver.add(team_assignment[0] != team_assignment[4])

# Constraint 4: Lateefah on Green team
solver.add(team_assignment[2] == 0)

# Constraint 5: Kelly not facilitator
solver.add(facilitator[1] == False)

# Constraint 6: Olga is facilitator
solver.add(facilitator[4] == True)

# Constraint 7: One facilitator per team
solver.add(PbEq([(And(team_assignment[s] == 0, facilitator[s]), 1) for s in range(5)], 1))
solver.add(PbEq([(And(team_assignment[s] == 1, facilitator[s]), 1) for s in range(5)], 1))


# Check answer choices
answer_choices = [
    And(facilitator[2] == True, team_assignment[2] == team_assignment[1]),
    And(facilitator[3] == True, team_assignment[3] == team_assignment[1]),
    And(facilitator[4] == True, team_assignment[4] == team_assignment[3]),
    And(facilitator[2] == True, team_assignment[2] != team_assignment[0]),
    And(facilitator[3] == True, team_assignment[3] != team_assignment[4])
]

for i, choice in enumerate(answer_choices):
    solver.push()
    solver.add(choice)
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()