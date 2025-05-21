from z3 import *

# Variables
team_assignment = Array('team_assignment', IntSort(), IntSort())
facilitator = Array('facilitator', IntSort(), BoolSort())

# Solver
solver = Solver()

# Constraints
s = Int('s')
solver.add(ForAll([s], And(team_assignment[s] >= 0, team_assignment[s] <= 1))) # Constraint 1
solver.add(team_assignment[0] != team_assignment[4]) # Constraint 2
solver.add(team_assignment[2] == 0) # Constraint 3
solver.add(Not(facilitator[1])) # Constraint 4
solver.add(facilitator[4]) # Constraint 5

green_facilitator_count = Sum([If(And(team_assignment[s] == 0, facilitator[s]), 1, 0) for s in range(5)])
red_facilitator_count = Sum([If(And(team_assignment[s] == 1, facilitator[s]), 1, 0) for s in range(5)])
solver.add(And(green_facilitator_count == 1, red_facilitator_count == 1)) # Constraint 6

green_team_size = Sum([If(team_assignment[s] == 0, 1, 0) for s in range(5)])
red_team_size = Sum([If(team_assignment[s] == 1, 1, 0) for s in range(5)])
solver.add(Or(And(green_team_size == 2, red_team_size == 3), And(green_team_size == 3, red_team_size == 2))) # Constraint 7


# Check answer choices
answer_choices = [
    team_assignment[0] == 0,  # A
    Not(facilitator[2]),  # B
    team_assignment[4] == 1,  # C
    And(facilitator[0], facilitator[3]),  # D
    Or(facilitator[0], facilitator[1])  # E
]
option_labels = ['A', 'B', 'C', 'D', 'E']

for i, choice in enumerate(answer_choices):
    solver.push()
    solver.add(Not(choice))
    if solver.check() == unsat:
        print(f"Option {option_labels[i]} is correct")
        exit()
    solver.pop()