from z3 import *

# Define variables
schedule = Array('schedule', IntSort(), IntSort())
i = Int('i')

# Create solver and add general constraints
solver = Solver()
solver.add(ForAll([i], Implies(And(i >= 0, i < 6), And(schedule[i] >= 0, schedule[i] < 6))))  # Domain
solver.add(Distinct([schedule[i] for i in range(6)]))  # Distinctness
solver.add(Or(And(schedule[0] == 1, schedule[1] == 5), And(schedule[0] == 5, schedule[1] == 1), And(schedule[2] == 1, schedule[3] == 5), And(schedule[2] == 5, schedule[3] == 1), And(schedule[4] == 1, schedule[5] == 5), And(schedule[4] == 5, schedule[5] == 1)))  # Kevin & Rebecca
solver.add(Not(Or(And(schedule[0] == 2, schedule[1] == 4), And(schedule[0] == 4, schedule[1] == 2), And(schedule[2] == 2, schedule[3] == 4), And(schedule[2] == 4, schedule[3] == 2), And(schedule[4] == 2, schedule[5] == 4), And(schedule[4] == 4, schedule[5] == 2))))  # Lan & Olivia
solver.add(Or(schedule[1] == 3, schedule[3] == 3, schedule[5] == 3))  # Nessa
solver.add(Or(And(schedule[0] == 0, Or(schedule[1] == 4, schedule[2] == 4, schedule[3] == 4, schedule[4] == 4, schedule[5] == 4)), And(schedule[1] == 0, Or(schedule[2] == 4, schedule[3] == 4, schedule[4] == 4, schedule[5] == 4)), And(schedule[2] == 0, Or(schedule[3] == 4, schedule[4] == 4, schedule[5] == 4)), And(schedule[3] == 0, Or(schedule[4] == 4, schedule[5] == 4))))  # Julio before Olivia

# Check answer choices
options = [
    [5, 1, 0, 2, 3, 4],  # A
    [4, 3, 0, 2, 1, 5],  # B
    [2, 1, 5, 0, 4, 3],  # C
    [1, 5, 0, 3, 4, 2],  # D
    [0, 2, 4, 3, 5, 1]   # E
]

for option_index, option in enumerate(options):
    solver.push()
    for slot, assistant in enumerate(option):
        solver.add(schedule[slot] == assistant)
    if solver.check() == sat:
        print(f"Option {chr(65 + option_index)} is correct")
        exit()
    solver.pop()