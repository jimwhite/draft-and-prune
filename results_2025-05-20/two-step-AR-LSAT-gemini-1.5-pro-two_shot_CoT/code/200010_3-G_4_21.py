from z3 import *

# Constants for breeds
H = 0
M = 1
S = 2
G = 0
N = 1
R = 2

# Variables
kitten_breed = Array('kitten_breed', IntSort(), IntSort())
puppy_breed = Array('puppy_breed', IntSort(), IntSort())

solver = Solver()

# Constraint 1: Breed Domains
for d in range(1, 8):
    solver.add(And(And(kitten_breed[d] >= 0, kitten_breed[d] <= 2), And(puppy_breed[d] >= 0, puppy_breed[d] <= 2)))

# Constraint 2 & 3: No Consecutive Breeds
for d in range(1, 7):
    solver.add(kitten_breed[d] != kitten_breed[d + 1])
    solver.add(puppy_breed[d] != puppy_breed[d + 1])

# Constraint 4 & 5: Day 1 and Day 7 Different
solver.add(kitten_breed[1] != kitten_breed[7])
solver.add(puppy_breed[1] != puppy_breed[7])

# Constraint 6: Greyhounds on Day 1
solver.add(puppy_breed[1] == G)

# Constraint 7: Himalayans Exactly Three Days
solver.add(Sum([If(kitten_breed[d] == H, 1, 0) for d in range(1, 8)]) == 3)

# Constraint 8: No Himalayans on Day 1
solver.add(kitten_breed[1] != H)

# Constraint 9: No Rottweilers on Day 7
solver.add(puppy_breed[7] != R)

# Constraint 10: No Rottweilers with Himalayans
for d in range(1, 8):
    solver.add(Implies(kitten_breed[d] == H, puppy_breed[d] != R))

# Check answer choices
answer_choices = [
    (puppy_breed[2] == G, kitten_breed[2] == S),  # A
    (puppy_breed[7] == G, kitten_breed[7] == H),  # B
    (puppy_breed[4] == R, kitten_breed[4] == H),  # C
    (puppy_breed[5] == R, kitten_breed[5] == M),  # D
    (puppy_breed[6] == N, kitten_breed[6] == M)   # E
]

for i, choice in enumerate(answer_choices):
    solver.push()
    solver.add(And(choice[0], choice[1]))
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()