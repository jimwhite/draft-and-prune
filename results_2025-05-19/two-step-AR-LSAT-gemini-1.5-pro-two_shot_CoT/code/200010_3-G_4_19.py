from z3 import *

# Define constants for breeds
H = 0  # Himalayan
M = 1  # Manx
S = 2  # Siamese
G = 0  # Greyhound
N = 1  # Newfoundland
R = 2  # Rottweiler

# Define Z3 variables
kitten_breed = Array('kitten_breed', IntSort(), IntSort())
puppy_breed = Array('puppy_breed', IntSort(), IntSort())
d = Int('d')

# Create solver
solver = Solver()

# Constraint 1: Breed domains
solver.add(ForAll(d, Implies(And(d >= 1, d <= 7), And(kitten_breed[d] >= 0, kitten_breed[d] < 3, puppy_breed[d] >= 0, puppy_breed[d] < 3))))

# Constraint 2: Greyhounds on Day 1
solver.add(puppy_breed[1] == G)

# Constraint 3 & 4: No consecutive breeds
solver.add(ForAll(d, Implies(And(d >= 1, d < 7), And(kitten_breed[d] != kitten_breed[d + 1], puppy_breed[d] != puppy_breed[d + 1]))))

# Constraint 5 & 6: No Day 1 breed on Day 7
solver.add(kitten_breed[1] != kitten_breed[7])
solver.add(puppy_breed[1] != puppy_breed[7])

# Constraint 7: Himalayans on exactly three days
solver.add(Sum([If(kitten_breed[d] == H, 1, 0) for d in range(1, 8)]) == 3)

# Constraint 8: No Himalayans on Day 1
solver.add(kitten_breed[1] != H)

# Constraint 9: No Rottweilers on Day 7
solver.add(puppy_breed[7] != R)

# Constraint 10: No Rottweilers with Himalayans
solver.add(ForAll(d, Implies(And(d >= 1, d <= 7), Implies(kitten_breed[d] == H, puppy_breed[d] != R))))

# Answer choices
choices = [
    [H, M, S, H, M, H, S],
    [M, H, S, H, M, H, M],
    [M, H, M, H, S, M, S],
    [S, H, M, H, S, S, H],
    [S, H, S, H, M, S, H]
]

# Check each answer choice
for i, choice in enumerate(choices):
    solver.push()
    for day in range(7):
        solver.add(kitten_breed[day + 1] == choice[day])
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()