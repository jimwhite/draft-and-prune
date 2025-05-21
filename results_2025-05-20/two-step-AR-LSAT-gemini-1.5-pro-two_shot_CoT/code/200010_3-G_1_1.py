from z3 import *

# Define variables
schedule = Array('schedule', IntSort(), IntSort())

# Create solver
solver = Solver()

# Constraint 1: Domain
i = Int('i')
solver.add(ForAll([i], Implies(And(i >= 0, i < 6), And(schedule[i] >= 0, schedule[i] < 8))))

# Constraint 2: Distinctness
solver.add(Distinct([schedule[i] for i in range(6)]))

# Constraint 3: Two reports per day (redundant but harmless)
day = Int('day')
solver.add(ForAll([day], Implies(And(day >= 0, day < 3), Distinct([schedule[day * 2], schedule[day * 2 + 1]]))))

# Constraint 4: George's schedule
solver.add(Or(schedule[2] == 0, schedule[3] == 0))

# Constraint 5: No Olivia/Robert in afternoon
solver.add(ForAll([day], Implies(And(day >= 0, day < 3), And(schedule[day * 2 + 1] != 6, schedule[day * 2 + 1] != 7))))

# Constraint 6: Nina's implication
solver.add(ForAll([day], Implies(And(day >= 0, day < 2), Implies(Or(schedule[day * 2] == 5, schedule[day * 2 + 1] == 5), And(Or(schedule[(day + 1) * 2] == 1, schedule[(day + 1) * 2 + 1] == 1), Or(schedule[(day + 1) * 2] == 2, schedule[(day + 1) * 2 + 1] == 2))))))

# Answer choices
choices = [
    [1, 7, 6, 2, 4, 3],  # A
    [2, 6, 1, 3, 5, 4],  # B
    [4, 1, 0, 3, 7, 2],  # C
    [5, 1, 7, 2, 6, 4],  # D
    [6, 5, 2, 1, 3, 0]   # E
]

# Check each answer choice
for option_index, choice in enumerate(choices):
    solver.push()
    for slot, student in enumerate(choice):
        solver.add(schedule[slot] == student)
    if solver.check() == sat:
        print(f"Option {chr(65 + option_index)} is correct")
        exit()
    solver.pop()