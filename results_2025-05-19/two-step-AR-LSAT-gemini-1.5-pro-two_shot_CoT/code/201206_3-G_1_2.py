from z3 import *

# Define variables
schedule = Array('schedule', IntSort(), IntSort())

# Create solver
solver = Solver()

# Constraint 0: Domain
i = Int('i')  # Define i before using it in ForAll
solver.add(ForAll([i], Implies(And(i >= 0, i < 6), And(schedule[i] >= 0, schedule[i] < 6))))

# Constraint 1: Distinctness
solver.add(Distinct([schedule[i] for i in range(6)]))

# Constraint 2: Kevin and Rebecca Same Day
solver.add(Or(
    And(schedule[0] == 1, schedule[1] == 5),
    And(schedule[0] == 5, schedule[1] == 1),
    And(schedule[2] == 1, schedule[3] == 5),
    And(schedule[2] == 5, schedule[3] == 1),
    And(schedule[4] == 1, schedule[5] == 5),
    And(schedule[4] == 5, schedule[5] == 1)
))

# Constraint 3: Lan and Olivia Different Days
i = Int('i')  # Redefine i and j for this constraint
j = Int('j')
solver.add(ForAll([i, j], Implies(And(i >= 0, i < 6, j >= 0, j < 6, i != j, schedule[i] == 2, schedule[j] == 4), Not(i / 2 == j / 2)))) # Use / instead of // for Z3

# Constraint 4: Nessa Afternoon
solver.add(Or(schedule[1] == 3, schedule[3] == 3, schedule[5] == 3))

# Constraint 5: Julio Before Olivia
i = Int('i')  # Redefine i and j for this constraint
j = Int('j')
solver.add(ForAll([i, j], Implies(And(i >= 0, i < 6, j >= 0, j < 6, schedule[i] == 0, schedule[j] == 4), i / 2 < j / 2))) # Use / instead of // for Z3


# Constraint 6: Lan Not Wednesday
solver.add(And(schedule[0] != 2, schedule[1] != 2))

# Answer choices and their corresponding IDs
answer_choices = ["Rebecca", "Olivia", "Nessa", "Kevin", "Julio"]
assistant_ids = [5, 4, 3, 1, 0]

# Check each answer choice
for choice_index, assistant_id in enumerate(assistant_ids):
    solver.push()
    solver.add(And(schedule[2] != assistant_id, schedule[3] != assistant_id))
    if solver.check() == unsat:
        print(f"Option {chr(65 + choice_index)} is correct")
        exit()
    solver.pop()
