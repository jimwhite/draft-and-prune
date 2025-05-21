from z3 import *

# Define variables
reviews = [[Int(f"reviews[{i}][{j}]") for j in range(3)] for i in range(5)]
solver = Solver()

# Constraint 1: Each student reviews at least one play
students = [0, 1, 2, 3, 4]
plays = [0, 1, 2]
for i in students:
    solver.add(Or([reviews[i][j] == 1 for j in plays]))

# Constraint 2: Kramer and Lopez review fewer plays than Megregian
solver.add(Sum([If(reviews[1][j] == 1, 1, 0) for j in plays]) < Sum([If(reviews[3][j] == 1, 1, 0) for j in plays]))
solver.add(Sum([If(reviews[2][j] == 1, 1, 0) for j in plays]) < Sum([If(reviews[3][j] == 1, 1, 0) for j in plays]))

# Constraint 3: Neither Lopez nor Megregian reviews any play Jiang reviews
for j in plays:
    solver.add(Implies(reviews[0][j] == 1, reviews[2][j] == 0))
    solver.add(Implies(reviews[0][j] == 1, reviews[3][j] == 0))

# Constraint 4: Kramer and O'Neill both review Tamerlane
solver.add(reviews[1][1] == 1)
solver.add(reviews[4][1] == 1)

# Constraint 5: Exactly two students review the same plays
solver.add(Sum([If(And([reviews[i][j] == reviews[k][j] for j in plays]), 1, 0) for i in students for k in range(i + 1, len(students))]) == 1)

# Add constraint: Jiang does not review Tamerlane
solver.add(reviews[0][1] == 0)

# Check answer choices
answer_choices = [
    (0, 0),  # Jiang reviews Sunset
    (2, 2),  # Lopez reviews Undulation
    (3, 0),  # Megregian reviews Sunset
    (3, 1),  # Megregian reviews Tamerlane
    (4, 2)   # O'Neill reviews Undulation
]
option_letter = 'A'
for student_id, play_id in answer_choices:
    solver.push()
    solver.add(reviews[student_id][play_id] == 0)
    if solver.check() == unsat:
        print(f"Option {option_letter} is correct")
        exit()
    solver.pop()
    option_letter = chr(ord(option_letter) + 1)

