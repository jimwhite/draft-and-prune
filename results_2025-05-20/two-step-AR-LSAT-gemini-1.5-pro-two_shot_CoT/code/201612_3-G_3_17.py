from z3 import *

# Variables
wall_pos_student = Array('wall_pos_student', IntSort(), IntSort())
wall_pos_painting_type = Array('wall_pos_painting_type', IntSort(), IntSort())
solver = Solver()

# Constraint 1: Domain constraints
for i in range(8):
    solver.add(And(wall_pos_student[i] >= 0, wall_pos_student[i] <= 3))
    solver.add(And(wall_pos_painting_type[i] >= 0, wall_pos_painting_type[i] <= 1))

# Constraint 2: Each student displays exactly one oil and one watercolor
for s in range(4):
    solver.add(Sum([If(And(wall_pos_student[i] == s, wall_pos_painting_type[i] == 0), 1, 0) for i in range(8)]) == 1)
    solver.add(Sum([If(And(wall_pos_student[i] == s, wall_pos_painting_type[i] == 1), 1, 0) for i in range(8)]) == 1)

# Constraint 4: No wall has only watercolors
for w in range(4):
    solver.add(Or(wall_pos_painting_type[w*2] == 0, wall_pos_painting_type[w*2 + 1] == 0))

# Constraint 5: No wall has work of only one student
for w in range(4):
    solver.add(wall_pos_student[w*2] != wall_pos_student[w*2 + 1])

# Constraint 6: No wall has both Franz and Isaacs
for w in range(4):
    solver.add(Not(And(Or(wall_pos_student[w*2] == 0, wall_pos_student[w*2 + 1] == 0), Or(wall_pos_student[w*2] == 3, wall_pos_student[w*2 + 1] == 3))))

# Constraint 7: Greene's watercolor with Franz's oil
i = Int('i')
solver.add(Exists(i, And(i >= 0, i <= 7, wall_pos_student[i] == 0, wall_pos_painting_type[i] == 0, wall_pos_student[(i / 2) * 2] == 1, wall_pos_painting_type[(i / 2) * 2] == 1)))


# Constraint 8: Isaacs's oil on wall 4 lower
solver.add(wall_pos_student[7] == 3)
solver.add(wall_pos_painting_type[7] == 0)

# Check answer choices
choices = [
    [And(wall_pos_student[i] == 0, i % 2 == 1) for i in range(8)], # Franz lower
    [And(wall_pos_student[i] == 1, i % 2 == 1) for i in range(8)], # Greene lower
    [And(wall_pos_student[i] == 2, i % 2 == 0) for i in range(8)], # Hidalgo upper
    [And(wall_pos_student[i] == 2, i % 2 == 1) for i in range(8)], # Hidalgo lower
    [And(wall_pos_student[i] == 1, i % 2 == 0) for i in range(8)]  # Greene upper
]

for option_idx, choice_constraints in enumerate([[0, 1], [0, 1], [0, 2], [1, 2], [1, 2]]):
    solver.push()
    student1 = choice_constraints[0]
    student2 = choice_constraints[1]
    position = option_idx < 2 if 1 else 0 if option_idx < 3 else 0
    for i in range(8):
        if i % 2 == position:
            solver.add(Or(wall_pos_student[i] == student1, wall_pos_student[i] == student1))
            solver.add(Or(wall_pos_student[i] == student2, wall_pos_student[i] == student2))

    if solver.check() == sat:
        print(f"Option {chr(65 + option_idx)} is correct")
        exit()
    solver.pop()