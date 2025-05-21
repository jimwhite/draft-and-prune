from z3 import *

# Define variables
team_assignment = Array('team_assignment', IntSort(), IntSort())
facilitator = Array('facilitator', IntSort(), BoolSort())
s = Int('s')

# Create solver and add constraints
solver = Solver()

# Constraint 1: Team Assignment Domain
solver.add(ForAll([s], And(team_assignment[s] >= 0, team_assignment[s] <= 1)))

# Constraint 2: Juana != Olga Team
solver.add(team_assignment[0] != team_assignment[4])

# Constraint 3: Lateefah on Green
solver.add(team_assignment[2] == 0)

# Constraint 4: Kelly not facilitator
solver.add(Not(facilitator[1]))

# Constraint 5: Olga is facilitator
solver.add(facilitator[4])

# Constraint 6: One facilitator per team
green_facilitator_count = Sum([If(And(team_assignment[i] == 0, facilitator[i]), 1, 0) for i in range(5)])
red_facilitator_count = Sum([If(And(team_assignment[i] == 1, facilitator[i]), 1, 0) for i in range(5)])
solver.add(And(green_facilitator_count == 1, red_facilitator_count == 1))

# Constraint 7: Team Sizes
green_team_size = Sum([If(team_assignment[i] == 0, 1, 0) for i in range(5)])
red_team_size = Sum([If(team_assignment[i] == 1, 1, 0) for i in range(5)])
solver.add(Or(And(green_team_size == 2, red_team_size == 3), And(green_team_size == 3, red_team_size == 2)))

# Check answer choices
options = [
    [[0, 2, 4], [4], [1, 3], [3]],  # A
    [[1, 2, 4], [2], [0, 3], [3]],  # B
    [[1, 2, 4], [4], [0, 3], [0]],  # C
    [[1, 3, 4], [4], [0, 2], [0]],  # D
    [[2, 4], [4], [0, 1, 3], [1]]   # E
]

for i, option in enumerate(options):
    solver.push()
    for student in option[0]:
        solver.add(team_assignment[student] == 0)
    for student in option[2]:
        solver.add(team_assignment[student] == 1)
    for student in option[1]:
        solver.add(facilitator[student])
    for student in option[3]:
        solver.add(facilitator[student])

    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()