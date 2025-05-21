from z3 import *

# Define variables
team_assignment = Array('team_assignment', IntSort(), IntSort())
facilitator = Array('facilitator', IntSort(), BoolSort())

solver = Solver()

# Constraint 1: Team Assignment
for s in range(5):
    solver.add(Or(team_assignment[s] == 0, team_assignment[s] == 1))

# Constraint 2: Juana/Olga different teams
solver.add(team_assignment[0] != team_assignment[4])

# Constraint 3: Lateefah on Green Team
solver.add(team_assignment[2] == 0)

# Constraint 4: Kelly not facilitator
solver.add(facilitator[1] == False)

# Constraint 5: Olga is facilitator
solver.add(facilitator[4] == True)

# Constraint 6: Exactly one facilitator per team
green_facilitator_count = Int('green_facilitator_count')
red_facilitator_count = Int('red_facilitator_count')
solver.add(green_facilitator_count == Sum([If(And(team_assignment[i] == 0, facilitator[i]), 1, 0) for i in range(5)]))
solver.add(red_facilitator_count == Sum([If(And(team_assignment[i] == 1, facilitator[i]), 1, 0) for i in range(5)]))
solver.add(And(green_facilitator_count == 1, red_facilitator_count == 1))

# Constraint 7: Team sizes
green_team_size = Int('green_team_size')
red_team_size = Int('red_team_size')
solver.add(green_team_size == Sum([If(team_assignment[i] == 0, 1, 0) for i in range(5)]))
solver.add(red_team_size == Sum([If(team_assignment[i] == 1, 1, 0) for i in range(5)]))
solver.add(Or(And(green_team_size == 2, red_team_size == 3), And(green_team_size == 3, red_team_size == 2)))

# Mei on Green Team
solver.add(team_assignment[3] == 0)

# Check answer choices
answer_choices = [
    team_assignment[0] != 0,  # A
    team_assignment[1] != 1,  # B
    team_assignment[4] != 0,  # C
    facilitator[2] == False,  # D
    facilitator[3] == False   # E
]

for i in range(len(answer_choices)):
    solver.push()
    solver.add(answer_choices[i])
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()