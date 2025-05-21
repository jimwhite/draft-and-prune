from z3 import *

# Define variables
team_assignment = Array('team_assignment', IntSort(), IntSort())
facilitator = Array('facilitator', IntSort(), BoolSort())

solver = Solver()

# Constraint 1: Team Assignment
for s in range(5):
    solver.add(Or(team_assignment[s] == 0, team_assignment[s] == 1))

# Constraint 2: Team Sizes
solver.add(Or(
    And(Sum([If(team_assignment[s] == 0, 1, 0) for s in range(5)]) == 2,
        Sum([If(team_assignment[s] == 1, 1, 0) for s in range(5)]) == 3),
    And(Sum([If(team_assignment[s] == 0, 1, 0) for s in range(5)]) == 3,
        Sum([If(team_assignment[s] == 1, 1, 0) for s in range(5)]) == 2)
))

# Constraint 3: One Facilitator per Team
solver.add(Sum([If(And(team_assignment[s] == 0, facilitator[s]), 1, 0) for s in range(5)]) == 1)
solver.add(Sum([If(And(team_assignment[s] == 1, facilitator[s]), 1, 0) for s in range(5)]) == 1)

# Constraint 4: Juana != Olga Team
solver.add(team_assignment[0] != team_assignment[4])

# Constraint 5: Lateefah on Green
solver.add(team_assignment[2] == 0)

# Constraint 6: Kelly not Facilitator
solver.add(Not(facilitator[1]))

# Constraint 7: Olga is Facilitator
solver.add(facilitator[4])

# Constraint 8: Lateefah is Facilitator
solver.add(facilitator[2])

# Check answer choices
answer_choices = [
    And(team_assignment[0] == 1, team_assignment[1] == 1),  # A
    And(team_assignment[0] == 1, team_assignment[3] == 1),  # B
    And(team_assignment[2] == 0, team_assignment[4] == 0),  # C
    And(team_assignment[3] == 0, team_assignment[4] == 0),  # D
    And(team_assignment[3] == 1, team_assignment[4] == 1)   # E
]

for i, choice in enumerate(answer_choices):
    solver.push()
    solver.add(choice)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()