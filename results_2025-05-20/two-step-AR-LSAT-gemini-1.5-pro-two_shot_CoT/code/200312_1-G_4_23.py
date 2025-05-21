from z3 import *

# Define variables
reviews = [[Bool(f"reviews[{i}][{j}]") for j in range(3)] for i in range(5)]

solver = Solver()

# Constraint 1: Each student reviews at least one play
for i in range(5):
    solver.add(Or(reviews[i][0], reviews[i][1], reviews[i][2]))

# Helper function to count plays reviewed by a student
def num_reviewed(s):
    return If(reviews[s][0], 1, 0) + If(reviews[s][1], 1, 0) + If(reviews[s][2], 1, 0)

# Constraint 2: Kramer and Lopez review fewer plays than Megregian
solver.add(num_reviewed(1) < num_reviewed(3))
solver.add(num_reviewed(2) < num_reviewed(3))

# Constraint 3: Neither Lopez nor Megregian reviews any play Jiang reviews
for j in range(3):
    solver.add(Implies(reviews[0][j], Not(reviews[2][j])))
    solver.add(Implies(reviews[0][j], Not(reviews[3][j])))

# Constraint 4: Kramer and O'Neill both review Tamerlane
solver.add(reviews[1][1])
solver.add(reviews[4][1])

# Helper function to check if two students review the same plays
def same_reviews(i, j):
    return And(reviews[i][0] == reviews[j][0], reviews[i][1] == reviews[j][1], reviews[i][2] == reviews[j][2])

# Constraint 5: Exactly two students review the same plays
same_reviews_pairs = [same_reviews(i, j) for i in range(5) for j in range(i + 1, 5)]
solver.add(PbEq([(pair, 1) for pair in same_reviews_pairs], 1))


# Premise: Jiang does not review Tamerlane
solver.add(Not(reviews[0][1]))

# Check answer choices
answer_choices = [
    Not(reviews[0][0]),  # A: Jiang reviews Sunset
    Not(reviews[2][2]),  # B: Lopez reviews Undulation
    Not(reviews[3][0]),  # C: Megregian reviews Sunset
    Not(reviews[3][1]),  # D: Megregian reviews Tamerlane
    Not(reviews[4][2])   # E: O'Neill reviews Undulation
]

for i, choice in enumerate(answer_choices):
    solver.push()
    solver.add(choice)
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()