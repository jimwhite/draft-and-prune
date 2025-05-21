from z3 import *

# Define variables
student_wall_position_painting = Array('student_wall_position_painting', IntSort(), IntSort(), IntSort(), IntSort(), BoolSort())
solver = Solver()

# Define constants for students (0: Franz, 1: Greene, 2: Hidalgo, 3: Isaacs)
Franz, Greene, Hidalgo, Isaacs = 0, 1, 2, 3
# Define constants for painting types (0: Oil, 1: Watercolor)
Oil, Watercolor = 0, 1
# Define constants for wall positions (0: Upper, 1: Lower)
Upper, Lower = 0, 1

# Number of students, walls, positions, types
num_students = 4
num_walls = 4
num_positions = 2
num_types = 2

# Constraint 1: Each student displays exactly two paintings (one oil and one watercolor)
solver.add(And([And(Sum([If(student_wall_position_painting[s][w][p][Oil], 1, 0) for w in range(num_walls) for p in range(num_positions)]) == 1,
                   Sum([If(student_wall_position_painting[s][w][p][Watercolor], 1, 0) for w in range(num_walls) for p in range(num_positions)]) == 1)
           for s in range(num_students)]))

# Constraint 2: Exactly two paintings are displayed on each wall (one upper and one lower)
solver.add(And([And(Sum([If(student_wall_position_painting[s][w][Upper][t], 1, 0) for s in range(num_students) for t in range(num_types)]) == 1,
                   Sum([If(student_wall_position_painting[s][w][Lower][t], 1, 0) for s in range(num_students) for t in range(num_types)]) == 1)
           for w in range(num_walls)]))

# Constraint 3: No wall has only watercolors
solver.add(And([Or([student_wall_position_painting[s][w][p][Oil] for s in range(num_students) for p in range(num_positions)])
           for w in range(num_walls)]))

# Constraint 4: No wall has the work of only one student
solver.add(And([Exists([s1, s2], And(s1 != s2,
                                      Or([student_wall_position_painting[s1][w][p][t] for p in range(num_positions) for t in range(num_types)]),
                                      Or([student_wall_position_painting[s2][w][p][t] for p in range(num_positions) for t in range(num_types)])))
           for w in range(num_walls)]))


# Constraint 5: No wall has both a painting by Franz and a painting by Isaacs
solver.add(And([Not(And(Or([student_wall_position_painting[Franz][w][p][t] for p in range(num_positions) for t in range(num_types)]),
                        Or([student_wall_position_painting[Isaacs][w][p][t] for p in range(num_positions) for t in range(num_types)])))
           for w in range(num_walls)]))

# Constraint 6: Greene's watercolor is displayed in the upper position of the wall on which Franz's oil is displayed
solver.add(And([Implies(Or([student_wall_position_painting[Franz][w][p][Oil] for p in range(num_positions)]), student_wall_position_painting[Greene][w][Upper][Watercolor])
           for w in range(num_walls)]))

# Constraint 7: Isaacs's oil is displayed in the lower position of wall 4
solver.add(student_wall_position_painting[Isaacs][3][Lower][Oil])

# Constraint 8: Greene's oil is displayed on the same wall as Franz's watercolor
solver.add(And([Implies(Or([student_wall_position_painting[Franz][w][p][Watercolor] for p in range(num_positions)]), Or([student_wall_position_painting[Greene][w][p][Oil] for p in range(num_positions)]))
           for w in range(num_walls)]))


# Check answer choices
answer_choices = [
    "Greene's oil is displayed in an upper position.",
    "Hidalgo's watercolor is displayed on the same wall as Isaacs's watercolor.",
    "Hidalgo's oil is displayed in an upper position.",
    "Hidalgo's oil is displayed on the same wall as Isaacs's watercolor.",
    "Isaacs's watercolor is displayed in a lower position."
]

for i, choice in enumerate(answer_choices):
    solver.push()
    if i == 0:
        solver.add(Not(Or([student_wall_position_painting[Greene][w][Upper][Oil] for w in range(num_walls)])))
    elif i == 1:
        solver.add(Not(Or([And(student_wall_position_painting[Hidalgo][w][p][Watercolor], student_wall_position_painting[Isaacs][w][_p][Watercolor]) for w in range(num_walls) for p in range(num_positions) for _p in range(num_positions)])))
    elif i == 2:
        solver.add(Not(Or([student_wall_position_painting[Hidalgo][w][Upper][Oil] for w in range(num_walls)])))
    elif i == 3:
        solver.add(Not(Or([And(student_wall_position_painting[Hidalgo][w][p][Oil], student_wall_position_painting[Isaacs][w][_p][Watercolor]) for w in range(num_walls) for p in range(num_positions) for _p in range(num_positions)])))
    elif i == 4:
        solver.add(Not(Or([student_wall_position_painting[Isaacs][w][Lower][Watercolor] for w in range(num_walls)])))

    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
