from z3 import *

# Define constants for breeds
H = 0
M = 1
S = 2
G = 3
N = 4
R = 5

# Define Z3 arrays for kitten and puppy breeds
kitten_breed = Array('k', IntSort(), IntSort())
puppy_breed = Array('p', IntSort(), IntSort())

# Create a Z3 solver
solver = Solver()

# Constraint 1 & 2: Breed Domain
for d in range(1, 8):
    solver.add(Or(kitten_breed[d] == H, kitten_breed[d] == M, kitten_breed[d] == S))
    solver.add(Or(puppy_breed[d] == G, puppy_breed[d] == N, puppy_breed[d] == R))

# Constraint 3 & 4: No Consecutive Breeds
for d in range(1, 7):
    solver.add(kitten_breed[d] != kitten_breed[d + 1])
    solver.add(puppy_breed[d] != puppy_breed[d + 1])

# Constraint 5 & 6: Day 1 and Day 7 Different
solver.add(kitten_breed[1] != kitten_breed[7])
solver.add(puppy_breed[1] != puppy_breed[7])

# Constraint 7: Greyhounds on Day 1
solver.add(puppy_breed[1] == G)

# Constraint 8: Himalayans Exactly Three Days
solver.add(Sum([If(kitten_breed[d] == H, 1, 0) for d in range(1, 8)]) == 3)

# Constraint 9: No Himalayans on Day 1
solver.add(kitten_breed[1] != H)

# Constraint 10: No Rottweilers on Day 7
solver.add(puppy_breed[7] != R)

# Constraint 11: No Rottweilers with Himalayans
for d in range(1, 8):
    solver.add(Implies(kitten_breed[d] == H, puppy_breed[d] != R))

# Add the condition from the question: No Himalayans on Day 7
solver.add(kitten_breed[7] != H)

# Check answer choices
choices = [
    "Greyhounds are featured on days 3 and 5.",
    "Newfoundlands are featured on day 3.",
    "Rottweilers are featured on day 6.",
    "Rottweilers are featured only on day 3.",
    "Rottweilers are featured on exactly three days."
]

for i, choice in enumerate(choices):
    solver.push()
    if i == 0:
        solver.add(And(puppy_breed[3] == G, puppy_breed[5] == G))
    elif i == 1:
        solver.add(puppy_breed[3] == N)
    elif i == 2:
        solver.add(puppy_breed[6] == R)
    elif i == 3:
        solver.add(And(puppy_breed[3] == R, ForAll([Int('d')], Implies(And(d >= 1, d <= 7, d != 3), puppy_breed[d] != R))))
    elif i == 4:
        solver.add(Sum([If(puppy_breed[d] == R, 1, 0) for d in range(1, 8)]) == 3)

    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()