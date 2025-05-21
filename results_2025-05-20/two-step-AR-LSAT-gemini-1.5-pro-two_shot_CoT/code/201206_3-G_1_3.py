from z3 import *

# Define variables
schedule = Array('schedule', IntSort(), IntSort())

# Define solver
solver = Solver()

# Base Constraints
solver.add(And([And(schedule[i] >= 0, schedule[i] < 6) for i in range(6)]))  # Domain
solver.add(Distinct([schedule[i] for i in range(6)]))  # Distinctness

# Kevin & Rebecca Same Day
solver.add(Or(
    And(schedule[0] == 1, schedule[1] == 5),
    And(schedule[2] == 1, schedule[3] == 5),
    And(schedule[4] == 1, schedule[5] == 5),
    And(schedule[0] == 5, schedule[1] == 1),
    And(schedule[2] == 5, schedule[3] == 1),
    And(schedule[4] == 5, schedule[5] == 1)
))

# Lan & Olivia Different Days
solver.add(Or(
    And(schedule[0] == 2, schedule[2] == 4),
    And(schedule[0] == 2, schedule[4] == 4),
    And(schedule[2] == 2, schedule[0] == 4),
    And(schedule[2] == 2, schedule[4] == 4),
    And(schedule[4] == 2, schedule[0] == 4),
    And(schedule[4] == 2, schedule[2] == 4)

))


# Nessa Afternoon
solver.add(Or(schedule[1] == 3, schedule[3] == 3, schedule[5] == 3))

# Julio before Olivia
solver.add(Implies(schedule[0] == 0, Or(schedule[2] == 4, schedule[4] == 4)))
solver.add(Implies(schedule[2] == 0, schedule[4] == 4))

# Additional Condition: Kevin before Nessa
solver.add(Implies(schedule[0] == 1, schedule[1] == 3))
solver.add(Implies(schedule[2] == 1, schedule[3] == 3))
solver.add(Implies(schedule[4] == 1, schedule[5] == 3))



# Answer Choices
options = [
    [0, 3],  # Julio, Nessa
    [1, 5],  # Kevin, Rebecca
    [1, 3, 5],  # Kevin, Nessa, Rebecca
    [0, 1, 3, 5],  # Julio, Kevin, Nessa, Rebecca
    [0, 1, 2, 3, 5]  # Julio, Kevin, Lan, Nessa, Rebecca
]
option_labels = ['A', 'B', 'C', 'D', 'E']

for option_index, option in enumerate(options):
    solver.push()
    possible = False
    for assistant in option:
        solver.push()
        solver.add(schedule[3] == assistant)
        if solver.check() == sat:
            possible = True
            solver.pop()
            break  # Found a possible assistant, no need to check others in this option
        solver.pop()
    if possible:
        print(f"Option {option_labels[option_index]} is correct")
        exit()
    solver.pop()

