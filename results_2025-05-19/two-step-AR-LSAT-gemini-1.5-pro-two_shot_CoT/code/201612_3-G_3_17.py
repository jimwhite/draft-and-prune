from z3 import *

# Variables
student_painting_wall_pos = Array('student_painting_wall_pos', IntSort(), IntSort())
wall_pos_student = Array('wall_pos_student', IntSort(), IntSort())

solver = Solver()

# Constraint 1: Each student displays exactly two paintings
for s in range(4):
    solver.add(Distinct([student_painting_wall_pos[s * 10 + p] for p in range(2)]))
    for p in range(2):
        solver.add(And(student_painting_wall_pos[s * 10 + p] >= 0, student_painting_wall_pos[s * 10 + p] <= 31))


# Constraint 2: Exactly two paintings on each wall
for w in range(4):
    solver.add(Distinct([wall_pos_student[w * 10 + p] for p in range(2)]))
    for p in range(2):
        solver.add(And(wall_pos_student[w * 10 + p] >= 0, wall_pos_student[w * 10 + p] <= 3))

# Helper function to extract wall and position
def get_wall_pos(val):
    return val // 10, val % 10

# Add constraints linking student_painting_wall_pos and wall_pos_student
for s in range(4):
    for p in range(2):
        for w in range(4):
            for pos in range(2):
                solver.add(Implies(student_painting_wall_pos[s * 10 + p] == w * 10 + pos, wall_pos_student[w * 10 + pos] == s))

# Constraint 3: No wall has only watercolors
# Use Sum and If to count students on each wall
for w in range(4):
    solver.add(Sum([If(student_painting_wall_pos[s * 10 + 0] / 10 == w, 1, 0) for s in range(4)]) + Sum([If(student_painting_wall_pos[s * 10 + 1] / 10 == w, 1, 0) for s in range(4)]) > 0) # Fixed: Use / instead of // for division


# Constraint 4: No wall has work of only one student
for w in range(4):
    solver.add(wall_pos_student[w * 10 + 0] != wall_pos_student[w * 10 + 1])

# Constraint 5: No wall has both Franz and Isaacs
for w in range(4):
    solver.add(Not(And(wall_pos_student[w * 10 + 0] == 0, wall_pos_student[w * 10 + 1] == 3)))
    solver.add(Not(And(wall_pos_student[w * 10 + 1] == 0, wall_pos_student[w * 10 + 0] == 3)))

# Constraint 6: Greene's watercolor with Franz's oil
solver.add(student_painting_wall_pos[1 * 10 + 1] / 10 == student_painting_wall_pos[0 * 10 + 0] / 10) # Fixed: Use / instead of //
solver.add(student_painting_wall_pos[1 * 10 + 1] % 10 == 0)


# Constraint 7: Isaacs's oil on wall 4 lower
solver.add(student_painting_wall_pos[3 * 10 + 0] == 3 * 10 + 1)

# Check answer choices
options = [
    "Both of Franz's paintings and both of Greene's paintings are displayed in lower positions.",
    "Both of Franz's paintings and both of Greene's paintings are displayed in upper positions.",
    "Both of Franz's paintings and both of Hidalgo's paintings are displayed in upper positions.",
    "Both of Greene's paintings and both of Hidalgo's paintings are displayed in lower positions.",
    "Both of Greene's paintings and both of Hidalgo's paintings are displayed in upper positions."
]

for i, option in enumerate(options):
    solver.push()
    if i == 0:
        solver.add(And(student_painting_wall_pos[0 * 10 + 0] % 10 == 1, student_painting_wall_pos[0 * 10 + 1] % 10 == 1))
        solver.add(And(student_painting_wall_pos[1 * 10 + 0] % 10 == 1, student_painting_wall_pos[1 * 10 + 1] % 10 == 1))
    elif i == 1:
        solver.add(And(student_painting_wall_pos[0 * 10 + 0] % 10 == 0, student_painting_wall_pos[0 * 10 + 1] % 10 == 0))
        solver.add(And(student_painting_wall_pos[1 * 10 + 0] % 10 == 0, student_painting_wall_pos[1 * 10 + 1] % 10 == 0))
    elif i == 2:
        solver.add(And(student_painting_wall_pos[0 * 10 + 0] % 10 == 0, student_painting_wall_pos[0 * 10 + 1] % 10 == 0))
        solver.add(And(student_painting_wall_pos[2 * 10 + 0] % 10 == 0, student_painting_wall_pos[2 * 10 + 1] % 10 == 0))
    elif i == 3:
        solver.add(And(student_painting_wall_pos[1 * 10 + 0] % 10 == 1, student_painting_wall_pos[1 * 10 + 1] % 10 == 1))
        solver.add(And(student_painting_wall_pos[2 * 10 + 0] % 10 == 1, student_painting_wall_pos[2 * 10 + 1] % 10 == 1))
    elif i == 4:
        solver.add(And(student_painting_wall_pos[1 * 10 + 0] % 10 == 0, student_painting_wall_pos[1 * 10 + 1] % 10 == 0))
        solver.add(And(student_painting_wall_pos[2 * 10 + 0] % 10 == 0, student_painting_wall_pos[2 * 10 + 1] % 10 == 0))

    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
