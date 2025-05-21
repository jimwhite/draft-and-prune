from z3 import *

# Constants for breeds
H, M, S = 0, 1, 2
G, N, R = 0, 1, 2

# Variables
kitten_breed = Array('kitten_breed', IntSort(), IntSort())
puppy_breed = Array('puppy_breed', IntSort(), IntSort())

solver = Solver()

# Constraint 1: Kitten and Puppy Breed Domains
for d in range(1, 8):
    solver.add(And(And(kitten_breed[d] >= 0, kitten_breed[d] <= 2), And(puppy_breed[d] >= 0, puppy_breed[d] <= 2)))

# Constraint 2: One Kitten and Puppy per Day
for d in range(1, 8):
    solver.add(Distinct(kitten_breed[d], puppy_breed[d]))

# Constraint 3: No Consecutive Breeds
for d in range(1, 7):
    solver.add(And(Distinct(kitten_breed[d], kitten_breed[d + 1]), Distinct(puppy_breed[d], puppy_breed[d + 1])))

# Constraint 4: Greyhounds on Day 1
solver.add(puppy_breed[1] == G)

# Constraint 5: No Day 1 Breed on Day 7
solver.add(And(Distinct(kitten_breed[1], kitten_breed[7]), Distinct(puppy_breed[1], puppy_breed[7])))

# Constraint 6: Himalayans on 3 Days, Not Day 1
solver.add(kitten_breed[1] != H)
solver.add(Sum([If(kitten_breed[d] == H, 1, 0) for d in range(1, 8)]) == 3)

# Constraint 7: No Rottweilers on Day 7 or with Himalayans
solver.add(puppy_breed[7] != R)
for d in range(1, 8):
    solver.add(Implies(kitten_breed[d] == H, puppy_breed[d] != R))

# Check answer choices
options = [
    And(puppy_breed[2] == G, kitten_breed[2] == S),
    And(puppy_breed[7] == G, kitten_breed[7] == H),
    And(puppy_breed[4] == R, kitten_breed[4] == H),
    And(puppy_breed[5] == R, kitten_breed[5] == M),
    And(puppy_breed[6] == N, kitten_breed[6] == M)
]

for i, option in enumerate(options):
    solver.push()
    solver.add(option)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()