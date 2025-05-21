from z3 import *

# Define variables
kitten_breed = Array('kitten_breed', IntSort(), IntSort())
puppy_breed = Array('puppy_breed', IntSort(), IntSort())

solver = Solver()

# Constants for breeds
H, M, S = 0, 1, 2
G, N, R = 0, 1, 2

# Constraint 1: Breed Domains
for d in range(1, 8):
    solver.add(And(0 <= kitten_breed[d], kitten_breed[d] <= 2))
    solver.add(And(0 <= puppy_breed[d], puppy_breed[d] <= 2))

# Constraint 2 & 3: No Consecutive Breeds
for d in range(1, 7):
    solver.add(kitten_breed[d] != kitten_breed[d + 1])
    solver.add(puppy_breed[d] != puppy_breed[d + 1])

# Constraint 4 & 5: Day 1 and Day 7 Different
solver.add(kitten_breed[1] != kitten_breed[7])
solver.add(puppy_breed[1] != puppy_breed[7])

# Constraint 6: Greyhounds on Day 1
solver.add(puppy_breed[1] == G)

# Constraint 7: Himalayans Exactly Three Days, Not Day 1
solver.add(Sum([If(kitten_breed[d] == H, 1, 0) for d in range(1, 8)]) == 3)
solver.add(kitten_breed[1] != H)

# Constraint 8: Rottweilers Not on Day 7, Not with Himalayans
solver.add(puppy_breed[7] != R)
for d in range(1, 8):
    solver.add(Implies(kitten_breed[d] == H, puppy_breed[d] != R))

# Answer choices
choices = [
    "Himalayan, Manx, Siamese, Himalayan, Manx, Himalayan, Siamese",
    "Manx, Himalayan, Siamese, Himalayan, Manx, Himalayan, Manx",
    "Manx, Himalayan, Manx, Himalayan, Siamese, Manx, Siamese",
    "Siamese, Himalayan, Manx, Himalayan, Siamese, Siamese, Himalayan",
    "Siamese, Himalayan, Siamese, Himalayan, Manx, Siamese, Himalayan"
]
breed_map = {"Himalayan": H, "Manx": M, "Siamese": S}

# Check each answer choice
for i, choice in enumerate(choices):
    solver.push()
    breed_list = [breed_map[breed] for breed in choice.split(', ')]
    for d in range(7):
        solver.add(kitten_breed[d + 1] == breed_list[d])
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()