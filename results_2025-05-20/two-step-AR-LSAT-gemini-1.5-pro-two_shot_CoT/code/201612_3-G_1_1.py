from z3 import *

# Define variables
team_assignment = Array('team_assignment', IntSort(), IntSort())
facilitator = Array('facilitator', IntSort(), BoolSort())

solver = Solver()

# Constraint 1: Exactly One Team per Student
for s in range(5):
    solver.add(Or(team_assignment[s] == 0, team_assignment[s] == 1))

# Constraint 2: Juana != Olga Team
solver.add(team_assignment[0] != team_assignment[4])

# Constraint 3: Lateefah on Green
solver.add(team_assignment[2] == 0)

# Constraint 4: Kelly not Facilitator
solver.add(facilitator[1] == False)

# Constraint 5: Olga is Facilitator
solver.add(facilitator[4] == True)

# Constraint 6: Exactly One Facilitator per Team
s = Int('s') # Declare 's' as an integer variable for use in quantifiers
solver.add(Exists([s], And(team_assignment[s] == 0, facilitator[s] == True)))  # Green Team: At least one
solver.add(Exists([s], And(team_assignment[s] == 1, facilitator[s] == True)))  # Red Team: At least one
for i in range(5):
    for j in range(5):
        if i != j:
            solver.add(Implies(And(team_assignment[i] == 0, team_assignment[j] == 0, facilitator[i] == True), facilitator[j] == False))  # Green Team: At most one
            solver.add(Implies(And(team_assignment[i] == 1, team_assignment[j] == 1, facilitator[j] == True), facilitator[i] == False))  # Red Team: At most one


# Constraint 7: Team Sizes
green_count = Sum([If(team_assignment[i] == 0, 1, 0) for i in range(5)])
red_count = Sum([If(team_assignment[i] == 1, 1, 0) for i in range(5)])
solver.add(Or(And(green_count == 2, red_count == 3), And(green_count == 3, red_count == 2)))

# Answer Choices
options = [
    ([0, 2, 4], [4], [1, 3], [3]),  # A
    ([1, 2, 4], [2], [0, 3], [3]),  # B
    ([1, 2, 4], [4], [0, 3], [0]),  # C
    ([1, 3, 4], [4], [0, 2], [0]),  # D
    ([2, 4], [4], [0, 1, 3], [1]),  # E
]

for option_index, (green_team, green_facilitator, red_team, red_facilitator) in enumerate(options):
    solver.push()
    for s in green_team:
        solver.add(team_assignment[s] == 0)
    for s in red_team:
        solver.add(team_assignment[s] == 1)
    for s in range(5):
        solver.add(facilitator[s] == (s in green_facilitator or s in red_facilitator))

    if solver.check() == sat:
        print(f"Option {chr(65 + option_index)} is correct")
        exit()
    solver.pop()
