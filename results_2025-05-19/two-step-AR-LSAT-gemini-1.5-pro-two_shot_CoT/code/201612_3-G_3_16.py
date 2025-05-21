from z3 import *

# Variables
student_wall_pos_painting = [[[Int("student_wall_pos_painting[%s,%s,%s]" % (s, w, p)) for p in range(2)] for w in range(4)] for s in range(4)]

solver = Solver()

# Constraint 1: Each student displays exactly two paintings
for s in range(4):
    solver.add(Sum([If(student_wall_pos_painting[s][w][p] >= 0, 1, 0) for w in range(4) for p in range(2)]) == 2)

# Constraint 2: Exactly two paintings per wall
for w in range(4):
    solver.add(Sum([If(student_wall_pos_painting[s][w][p] >= 0, 1, 0) for s in range(4) for p in range(2)]) == 2)

# Constraint 3: Each student displays one oil and one watercolor
for s in range(4):
    solver.add(Sum([If(student_wall_pos_painting[s][w][p] == 0, 1, 0) for w in range(4) for p in range(2)]) == 1)
    solver.add(Sum([If(student_wall_pos_painting[s][w][p] == 1, 1, 0) for w in range(4) for p in range(2)]) == 1)

# Constraint 4: No wall has only watercolors
for w in range(4):
    solver.add(Or([student_wall_pos_painting[s][w][p] == 0 for s in range(4) for p in range(2)]))

# Constraint 5: No wall has work of only one student
for w in range(4):
    solver.add(Exists([s1, s2], And(Distinct(s1, s2), And(s1 >= 0, s1 < 4, s2 >= 0, s2 < 4), Or([And(student_wall_pos_painting[s1][w][p] >= 0, student_wall_pos_painting[s2][w][p] >= 0) for p in range(2)]))))

# Constraint 6: No wall has both Franz and Isaacs
for w in range(4):
    solver.add(Not(And(Or([student_wall_pos_painting[0][w][p] >= 0 for p in range(2)]), Or([student_wall_pos_painting[3][w][p] >= 0 for p in range(2)]))))


# Constraint 8: Isaacs's oil is on wall 4, lower
solver.add(student_wall_pos_painting[3][3][1] == 0)

# Constraint 9: Franz's oil is on wall 1
solver.add(student_wall_pos_painting[0][0][1] == 0)

# Check answer choices
options = [
    student_wall_pos_painting[0][3][0] == 1,  # A
    student_wall_pos_painting[1][1][0] == 0,  # B
    student_wall_pos_painting[1][1][0] == 1,  # C
    student_wall_pos_painting[2][2][0] == 1,  # D
    student_wall_pos_painting[3][0][0] == 0   # E
]
option_labels = ['A', 'B', 'C', 'D', 'E']

for i, option in enumerate(options):
    solver.push()
    solver.add(option)
    if solver.check() == sat:
        print(f"Option {option_labels[i]} is correct")
        exit()
    solver.pop()
