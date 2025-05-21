from z3 import *

# Variables
team_assignment = Array('team_assignment', IntSort(), IntSort())
facilitator = Array('facilitator', IntSort(), BoolSort())

solver = Solver()

# Constraints 1-7
for s in range(5):
    solver.add(And(team_assignment[s] >= 0, team_assignment[s] <= 1))

solver.add(team_assignment[0] != team_assignment[4])
solver.add(team_assignment[2] == 0)
solver.add(Not(facilitator[1]))
solver.add(facilitator[4])

green_facilitator_count = Sum([If(And(team_assignment[s] == 0, facilitator[s]), 1, 0) for s in range(5)])
red_facilitator_count = Sum([If(And(team_assignment[s] == 1, facilitator[s]), 1, 0) for s in range(5)])
solver.add(And(green_facilitator_count == 1, red_facilitator_count == 1))

green_team_size = Sum([If(team_assignment[s] == 0, 1, 0) for s in range(5)])
red_team_size = Sum([If(team_assignment[s] == 1, 1, 0) for s in range(5)])
solver.add(Or(And(green_team_size == 2, red_team_size == 3), And(green_team_size == 3, red_team_size == 2)))


# Check answer choices
answer_choices = [
    And(facilitator[2], team_assignment[2] == team_assignment[1]),
    And(facilitator[3], team_assignment[3] == team_assignment[1]),
    And(facilitator[4], team_assignment[4] == team_assignment[3]),
    And(facilitator[2], team_assignment[2] != team_assignment[0]),
    And(facilitator[3], team_assignment[3] != team_assignment[4])
]

for i, choice in enumerate(answer_choices):
    solver.push()
    solver.add(choice)
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()