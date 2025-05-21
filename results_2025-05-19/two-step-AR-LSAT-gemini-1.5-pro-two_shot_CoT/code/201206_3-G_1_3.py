from z3 import *

# Define variables
schedule = Array('schedule', IntSort(), IntSort())
i = Int('i')
j = Int('j')

# Create solver and add constraints
solver = Solver()

# Constraint 0 (Domain)
solver.add(ForAll([i], And(schedule[i] >= 0, schedule[i] < 6)))

# Constraint 1 (Distinctness)
solver.add(Distinct([schedule[i] for i in range(6)]))

# Constraint 2 (Kevin & Rebecca Same Day)
solver.add(Or(
    And(schedule[0] == 1, schedule[1] == 5),
    And(schedule[2] == 1, schedule[3] == 5),
    And(schedule[4] == 1, schedule[5] == 5),
    And(schedule[0] == 5, schedule[1] == 1),
    And(schedule[2] == 5, schedule[3] == 1),
    And(schedule[4] == 5, schedule[5] == 1)
))

# Constraint 3 (Lan & Olivia Different Days)
solver.add(Or(
    Not(Or(schedule[0] == 2, schedule[0] == 4, schedule[1] == 2, schedule[1] == 4)),
    Not(Or(schedule[2] == 2, schedule[2] == 4, schedule[3] == 2, schedule[3] == 4)),
    Not(Or(schedule[4] == 2, schedule[4] == 4, schedule[5] == 2, schedule[5] == 4))
))

# Constraint 4 (Nessa Afternoon)
solver.add(Or(schedule[1] == 3, schedule[3] == 3, schedule[5] == 3))

# Constraint 5 (Julio before Olivia) - Fixed integer division
solver.add(ForAll([i, j], Implies(And(schedule[i] == 0, schedule[j] == 4, i != j), i / 2 < j / 2)))


# Constraint 6-8 (Kevin before Nessa)
solver.add(Implies(schedule[0] == 1, Not(Or(schedule[1] == 3, schedule[3] == 3, schedule[5] == 3))))
solver.add(Implies(schedule[2] == 1, Not(Or(schedule[3] == 3, schedule[5] == 3))))
solver.add(Implies(schedule[4] == 1, Not(schedule[5] == 3)))


# Answer choices
choices = [
    [0, 3],  # Julio, Nessa
    [1, 5],  # Kevin, Rebecca
    [1, 3, 5],  # Kevin, Nessa, Rebecca
    [0, 1, 3, 5],  # Julio, Kevin, Nessa, Rebecca
    [0, 1, 2, 3, 5]  # Julio, Kevin, Lan, Nessa, Rebecca
]

# Check each answer choice
for idx, choice in enumerate(choices):
    solver.push()
    solver.add(Or([schedule[3] == assistant for assistant in choice]))
    if solver.check() == sat:
        possible_answer = chr(65 + idx)
    solver.pop()

    solver.push()
    solver.add(And([schedule[3] != assistant for assistant in choice]))
    if solver.check() == unsat:
        print(f"Option {possible_answer} is correct")
        exit()
    solver.pop()
