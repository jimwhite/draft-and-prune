from z3 import *

# Variables
reviews = [[Bool(f"reviews[{s}][{p}]") for p in range(3)] for s in range(5)]

# Solver
solver = Solver()

# Constraints

# Constraint 1: Each student reviews at least one play
for s in range(5):
    solver.add(Or([reviews[s][p] for p in range(3)]))

# Helper function to count reviews
num_reviews = lambda s: Sum([If(reviews[s][p], 1, 0) for p in range(3)])

# Constraint 2: Kramer and Lopez review fewer plays than Megregian
solver.add(num_reviews(1) < num_reviews(3))
solver.add(num_reviews(2) < num_reviews(3))

# Constraint 3: Neither Lopez nor Megregian reviews any play Jiang reviews
for p in range(3):
    solver.add(Implies(reviews[0][p], Not(reviews[2][p])))
    solver.add(Implies(reviews[0][p], Not(reviews[3][p])))

# Constraint 4: Kramer and O'Neill both review Tamerlane
solver.add(reviews[1][1])
solver.add(reviews[4][1])

# Constraint 5: Exactly two students review the same plays
solver.add(PbEq([(And(ForAll([Int('p')], reviews[i][p] == reviews[j][p]), i != j), 1) for i in range(5) for j in range(5)], 2))


# Check answer choices
options = [
    num_reviews(0) > num_reviews(2),  # A
    num_reviews(3) > num_reviews(0),  # B
    num_reviews(3) > num_reviews(4),  # C
    num_reviews(4) > num_reviews(0),  # D
    num_reviews(4) > num_reviews(1)   # E
]

for i, option in enumerate(options):
    solver.push()
    solver.add(Not(option))
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
