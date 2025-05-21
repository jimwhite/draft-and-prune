from z3 import *

# Define variables
schedule = Array('schedule', IntSort(), IntSort())

# Create solver
solver = Solver()

# Constraint 0 (Domain)
i = Int('i')
solver.add(ForAll([i], Implies(And(i >= 0, i < 7), And(schedule[i] >= 0, schedule[i] < 7))))

# Constraint 1 (Distinctness)
solver.add(Distinct([schedule[i] for i in range(7)]))

# Constraint 2 (J in Evening)
solver.add(Or(schedule[5] == 0, schedule[6] == 0))

# Constraint 3 (K not in Morning)
solver.add(Not(Or(schedule[0] == 1, schedule[1] == 1)))

# Constraint 4 (L before M)
i = Int('i')
j = Int('j')
solver.add(ForAll([i, j], Implies(And(i < j, i >= 0, i < 7, j >= 0, j < 7), Implies(And(schedule[i] == 2, schedule[j] == 3), i < j))))

# Constraint 5 (K before L)
i = Int('i')
j = Int('j')
solver.add(ForAll([i, j], Implies(And(i < j, i >= 0, i < 7, j >= 0, j < 7), Implies(And(schedule[i] == 1, schedule[j] == 2), i < j))))


# Answer choices
options = [(0, 1), (0, 3), (0, 5), (0, 6), (3, 6)]
option_letters = ['A', 'B', 'C', 'D', 'E']

# Check each answer choice
for idx, (house1, house2) in enumerate(options):
    solver.push()
    consecutive = []
    for i in range(6):
        consecutive.append(Or(And(schedule[i] == house1, schedule[i+1] == house2), And(schedule[i] == house2, schedule[i+1] == house1)))
    solver.add(Or(consecutive))

    if solver.check() == unsat:
        print(f"Option {option_letters[idx]} is correct")
        exit()
    solver.pop()