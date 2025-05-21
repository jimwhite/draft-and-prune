from z3 import *

# Define variables
schedule = Array('schedule', IntSort(), IntSort())
solver = Solver()
i = Int('i')

# Constraint 1 (Domain)
solver.add(ForAll([i], And(schedule[i] >= 0, schedule[i] < 8)))

# Constraint 2 (Distinctness)
solver.add(Distinct([schedule[i] for i in range(6)]))

# Constraint 3 (George's schedule)
solver.add(schedule[3] == 0)

# Constraint 4 (Olivia/Robert afternoon)
solver.add(Not(Or(schedule[1] == 6, schedule[3] == 6, schedule[5] == 6)))
solver.add(Not(Or(schedule[1] == 7, schedule[3] == 7, schedule[5] == 7)))

# Constraint 5 (Nina's implication)
solver.add(Implies(schedule[0] == 5, Or(And(schedule[2] == 1, schedule[3] == 2), And(schedule[2] == 2, schedule[3] == 1))))
solver.add(Implies(schedule[1] == 5, Or(And(schedule[2] == 1, schedule[3] == 2), And(schedule[2] == 2, schedule[3] == 1))))
solver.add(Implies(schedule[2] == 5, Or(And(schedule[4] == 1, schedule[5] == 2), And(schedule[4] == 2, schedule[5] == 1))))
solver.add(Implies(schedule[3] == 5, Or(And(schedule[4] == 1, schedule[5] == 2), And(schedule[4] == 2, schedule[5] == 1))))
solver.add(Implies(Or(schedule[4] == 5, schedule[5] == 5), True))

# Question constraints
solver.add(schedule[3] == 3)
solver.add(schedule[5] == 1)

# Answer choices
choices = [
    [2, 4, 5],  # Irving, Lenore, Nina
    [4, 0, 2],  # Lenore, George, Irving
    [5, 2, 4],  # Nina, Irving, Lenore
    [7, 0, 2],  # Robert, George, Irving
    [7, 2, 4]   # Robert, Irving, Lenore
]

for i, choice in enumerate(choices):
    solver.push()
    solver.add(schedule[0] == choice[0])
    solver.add(schedule[2] == choice[1])
    solver.add(schedule[4] == choice[2])
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()