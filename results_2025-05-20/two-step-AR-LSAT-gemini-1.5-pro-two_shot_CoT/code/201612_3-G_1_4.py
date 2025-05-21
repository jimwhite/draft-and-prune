from z3 import *

# Define variables
team_assignment = Array('team_assignment', IntSort(), IntSort())
facilitator = Array('facilitator', IntSort(), BoolSort())

# Create solver
solver = Solver()

# Constraint 1: Team Assignment
s = Int('s')
solver.add(ForAll([s], Implies(And(s >= 0, s < 5), And(team_assignment[s] >= 0, team_assignment[s] <= 1))))

# Constraint 2: Exactly One Facilitator per Team
green_facilitator_count = Sum([If(And(team_assignment[i] == 0, facilitator[i]), 1, 0) for i in range(5)])
red_facilitator_count = Sum([If(And(team_assignment[i] == 1, facilitator[i]), 1, 0) for i in range(5)])
solver.add(green_facilitator_count == 1)
solver.add(red_facilitator_count == 1)

# Constraint 3: Team Sizes
green_team_size = Sum([If(team_assignment[i] == 0, 1, 0) for i in range(5)])
red_team_size = Sum([If(team_assignment[i] == 1, 1, 0) for i in range(5)])
solver.add(Or(And(green_team_size == 2, red_team_size == 3), And(green_team_size == 3, red_team_size == 2)))

# Constraint 4: Juana and Olga different teams
solver.add(team_assignment[0] != team_assignment[4])

# Constraint 5: Lateefah on Green team
solver.add(team_assignment[2] == 0)

# Constraint 6: Kelly not facilitator
solver.add(Not(facilitator[1]))

# Constraint 7: Olga is facilitator
solver.add(facilitator[4])

# Question Premise: Lateefah is facilitator
solver.add(facilitator[2])

# Answer Choices
choices = [
    And(team_assignment[0] == 1, team_assignment[1] == 1),  # A
    And(team_assignment[0] == 1, team_assignment[3] == 1),  # B
    And(team_assignment[2] == 0, team_assignment[4] == 0),  # C
    And(team_assignment[3] == 0, team_assignment[4] == 0),  # D
    And(team_assignment[3] == 1, team_assignment[4] == 1)   # E
]

for i, choice in enumerate(choices):
    solver.push()
    solver.add(choice)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()