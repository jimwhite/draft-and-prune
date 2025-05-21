from z3 import *

# Define variables
space = Array('space', IntSort(), IntSort())
i = Int('i')
j = Int('j')

# Define solver and add constraints
solver = Solver()

# Constraint 1 (Domain)
solver.add(ForAll([i], Implies(And(i >= 1, i <= 7), And(space[i] >= 0, space[i] <= 6))))

# Constraint 2 (Distinctness)
solver.add(Distinct([space[i] for i in range(1, 8)]))

# Constraint 3 & 4 (Pharmacy at one end, Restaurant at other)
solver.add(Or(space[1] == 1, space[7] == 1))
solver.add(Or(space[1] == 2, space[1] == 3, space[7] == 2, space[7] == 3))
solver.add(space[1] != space[7])


# Constraint 5 (Restaurants Separated)
solver.add(ForAll([i], Implies(And(i >= 1, i <= 6), Not(And(Or(space[i] == 2, space[i] == 3), Or(space[i+1] == 2, space[i+1] == 3))))))
solver.add(ForAll([i], Implies(And(i >= 1, i <= 5), Not(And(Or(space[i] == 2, space[i] == 3), Or(space[i+2] == 2, space[i+2] == 3))))))


# Constraint 6 (Pharmacy Next to O or V)
solver.add(Implies(space[1] == 1, Or(space[2] == 0, space[2] == 6)))
solver.add(Implies(space[7] == 1, Or(space[6] == 0, space[6] == 6)))

# Constraint 7 (Toy Store Not Next to V)
solver.add(ForAll([i], Implies(And(i >= 1, i <= 6), Not(Or(And(space[i] == 5, space[i+1] == 6), And(space[i] == 6, space[i+1] == 5))))))

# Answer choices
options = [
    [1, 0, 4, 2, 6, 5, 3],  # A
    [1, 6, 0, 4, 2, 5, 3],  # B
    [2, 4, 6, 1, 0, 5, 3],  # C
    [2, 5, 0, 3, 6, 4, 1],  # D
    [2, 0, 5, 3, 4, 6, 1]   # E
]

# Check each option
for option_index, option in enumerate(options):
    solver.push()
    for i in range(7):
        solver.add(space[i+1] == option[i])
    if solver.check() == sat:
        print(f"Option {chr(65 + option_index)} is correct")
        exit()
    solver.pop()