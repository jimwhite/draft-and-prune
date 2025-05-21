from z3 import *

# Define variables
schedule = Array('schedule', IntSort(), IntSort())

# Create solver
solver = Solver()

# Constraint 0: Domain
i = Int('i')  # Define i
solver.add(ForAll([i], Implies(And(i >= 0, i < 6), And(schedule[i] >= 0, schedule[i] < 6))))

# Constraint 1: Distinctness
solver.add(Distinct([schedule[i] for i in range(6)]))

# Constraint 2: Kevin and Rebecca Same Day
solver.add(Or(
    And(schedule[0] == 1, schedule[1] == 5), And(schedule[0] == 5, schedule[1] == 1),
    And(schedule[2] == 1, schedule[3] == 5), And(schedule[2] == 5, schedule[3] == 1),
    And(schedule[4] == 1, schedule[5] == 5), And(schedule[4] == 5, schedule[5] == 1)
))

# Constraint 3: Lan and Olivia Different Days
solver.add(Not(Or(
    And(schedule[0] == 2, schedule[1] == 4), And(schedule[0] == 4, schedule[1] == 2),
    And(schedule[2] == 2, schedule[3] == 4), And(schedule[2] == 4, schedule[3] == 2),
    And(schedule[4] == 2, schedule[5] == 4), And(schedule[4] == 4, schedule[5] == 2)
)))

# Constraint 4: Nessa Afternoon
solver.add(Or(schedule[1] == 3, schedule[3] == 3, schedule[5] == 3))

# Constraint 5: Julio before Olivia
j = Int('j')
k = Int('k')
solver.add(ForAll([j, k], Implies(And(j >= 0, j < 6, k >= 0, k < 6, schedule[j] == 0, schedule[k] == 4), j < k)))


# Answer choices
choices = [
    [5, 1, 0, 2, 3, 4],  # A
    [4, 3, 0, 2, 1, 5],  # B
    [2, 1, 5, 0, 4, 3],  # C
    [1, 5, 0, 3, 4, 2],  # D
    [0, 2, 4, 3, 5, 1]   # E
]

# Check each choice
for i, choice in enumerate(choices):
    solver.push()
    for slot in range(6):
        solver.add(schedule[slot] == choice[slot])
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
