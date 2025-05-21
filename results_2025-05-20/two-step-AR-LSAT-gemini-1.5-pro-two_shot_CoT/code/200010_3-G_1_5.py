from z3 import *

# Define variables
schedule = Array('schedule', IntSort(), IntSort())
solver = Solver()

# Constraint 1 (Domain)
i = Int('i')
solver.add(ForAll([i], Implies(And(i >= 0, i < 6), And(schedule[i] >= 0, schedule[i] < 8))))

# Constraint 2 (Distinctness)
solver.add(Distinct([schedule[i] for i in range(6)]))

# Constraint 3 (Two reports per day)
day = Int('day')
solver.add(ForAll([day], Implies(And(day >= 0, day < 3), Distinct([schedule[day * 2], schedule[day * 2 + 1]]))))

# Constraint 4 (George's schedule)
solver.add(Or(schedule[2] == 0, schedule[3] == 0))

# Constraint 5 (No Olivia/Robert in afternoon)
solver.add(ForAll([day], Implies(And(day >= 0, day < 3), And(schedule[day * 2 + 1] != 6, schedule[day * 2 + 1] != 7))))

# Constraint 6 (Nina's implication)
solver.add(ForAll([day], Implies(And(day >= 0, day < 2), Implies(Or(schedule[day * 2] == 5, schedule[day * 2 + 1] == 5), And(Or(schedule[(day + 1) * 2] == 1, schedule[(day + 1) * 2 + 1] == 1), Or(schedule[(day + 1) * 2] == 2, schedule[(day + 1) * 2 + 1] == 2))))))


# Kyle's Tuesday afternoon constraint
solver.add(schedule[3] == 3)

# Helen's Wednesday afternoon constraint
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