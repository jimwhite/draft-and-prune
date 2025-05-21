from z3 import *

# Define variables
schedule = Array('schedule', IntSort(), IntSort())

# Define solver and add constraints
solver = Solver()

# Constraint 0 (Domain)
solver.add([And(schedule[i] >= 0, schedule[i] < 7) for i in range(7)])

# Constraint 1 (Distinctness)
solver.add(Distinct([schedule[i] for i in range(7)]))

# Constraint 2 (J in Evening)
solver.add(Or(schedule[5] == 0, schedule[6] == 0))

# Constraint 3 (K not in Morning)
solver.add(And(schedule[0] != 1, schedule[1] != 1))

# Constraint 4 (L before M)
i, j = Ints('i j')
solver.add(ForAll([i, j], Implies(And(i >= 0, i < 7, j >= 0, j < 7, schedule[i] == 2, schedule[j] == 3), i < j)))

# Constraint 5 (K before L)
solver.add(ForAll([i, j], Implies(And(i >= 0, i < 7, j >= 0, j < 7, schedule[i] == 1, schedule[j] == 2), i < j)))


# Check answer choices
answer_choices = [
    (0, 1),  # J, K
    (0, 3),  # J, M
    (0, 5),  # J, O
    (0, 6),  # J, P
    (3, 6)   # M, P
]

for option_index, (house1_idx, house2_idx) in enumerate(answer_choices):
    solver.push()
    i = Int('i')
    solver.add(Exists(i, And(i >= 0, i < 6, Or(And(schedule[i] == house1_idx, schedule[i+1] == house2_idx), And(schedule[i] == house2_idx, schedule[i+1] == house1_idx)))))
    if solver.check() == unsat:
        print(f"Option {chr(65 + option_index)} is correct")
        exit()
    solver.pop()