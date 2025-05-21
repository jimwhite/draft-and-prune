from z3 import *

# Define variables for businesses
O, P, R1, R2, S, T, V = Ints('O P R1 R2 S T V')
businesses = [O, P, R1, R2, S, T, V]

# Define the mapping from space to business
space = Array('space', IntSort(), IntSort())

solver = Solver()

# Constraint 1: Distinctness
solver.add(Distinct(businesses))
for i in range(1, 8):
    solver.add(Or([space[i] == b for b in businesses]))
    for j in range(1, 8):
        if i != j:
            solver.add(Implies(space[i] == space[j], i == j))


# Constraint 2: Pharmacy at End
solver.add(Or(space[1] == P, space[7] == P))

# Constraint 3: Restaurant at Other End
solver.add(Or(space[1] == R1, space[1] == R2, space[7] == R1, space[7] == R2))
solver.add(Implies(space[1] == P, Or(space[7] == R1, space[7] == R2)))
solver.add(Implies(space[7] == P, Or(space[1] == R1, space[1] == R2)))

# Constraint 4: Restaurants Separated
solver.add(Implies(And(space[1] == R1, space[7] == R2), True)) # Trivial case
solver.add(Implies(And(space[1] == R2, space[7] == R1), True)) # Trivial case
for i in range(1, 8):
    for j in range(1, 8):
        if i != j:
            solver.add(Implies(And(Or(space[i] == R1, space[i] == R2), Or(space[j] == R1, space[j] == R2), Not(space[i] == space[j])), Abs(i - j) >= 3))


# Constraint 5: Pharmacy Next to O or V
for i in range(1, 8):
    solver.add(Implies(space[i] == P, Or(And(i > 1, Or(space[i-1] == O, space[i-1] == V)), And(i < 7, Or(space[i+1] == O, space[i+1] == V)))))

# Constraint 6: Toy Store Not Next to V
for i in range(1, 8):
    solver.add(Implies(space[i] == T, And(Implies(i > 1, space[i-1] != V), Implies(i < 7, space[i+1] != V))))

# Constraint 7: Veterinarian in Space 5
solver.add(space[5] == V)

# Check answer choices
options = [
    space[2] == O,  # A
    space[7] == P,  # B
    Or(space[4] == R1, space[4] == R2),  # C
    space[6] == S,  # D
    space[3] == T   # E
]

for i, option in enumerate(options):
    solver.push()
    solver.add(Not(option))
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()