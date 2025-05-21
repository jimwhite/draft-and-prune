from z3 import *

# Define variables
students = 5
plays = 3
reviews = [[Bool(f"reviews[{i}][{j}]") for j in range(plays)] for i in range(students)]
solver = Solver()

# Constraint 1: Each student reviews at least one play
for i in range(students):
    solver.add(Or(reviews[i]))

# Constraint 2: Kramer and Lopez review fewer plays than Megregian
solver.add(Sum([If(reviews[1][j], 1, 0) for j in range(plays)]) < Sum([If(reviews[3][j], 1, 0) for j in range(plays)]))
solver.add(Sum([If(reviews[2][j], 1, 0) for j in range(plays)]) < Sum([If(reviews[3][j], 1, 0) for j in range(plays)]))

# Constraint 3: Neither Lopez nor Megregian reviews any play Jiang reviews
for j in range(plays):
    solver.add(Implies(reviews[0][j], Not(reviews[2][j])))
    solver.add(Implies(reviews[0][j], Not(reviews[3][j])))

# Constraint 4: Kramer and O'Neill both review Tamerlane
solver.add(reviews[1][1])
solver.add(reviews[4][1])

# Constraint 5: Exactly two students review the same plays
solver.add(Sum([If(And(Sum([If(reviews[i][k] == reviews[j][k], 1, 0) for k in range(plays)]) == plays, i < j), 1, 0) for i in range(students) for j in range(students)]) == 1)

# Answer choices
options = [
    [2],
    [4],
    [0, 2],
    [1, 4],
    [2, 3]
]

for option_index, option in enumerate(options):
    solver.push()
    for student_id in option:
        solver.add(reviews[student_id][0])
        solver.add(Not(reviews[student_id][1]))
        solver.add(Not(reviews[student_id][2]))
    for student_id in range(students):
        if student_id not in option:
            solver.add(Or(reviews[student_id][1], reviews[student_id][2]))

    if solver.check() == sat:
        print(f"Option {chr(65 + option_index)} is correct")
        exit()
    solver.pop()
