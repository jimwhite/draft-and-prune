from z3 import *

# Define students, types, walls, and positions
students = {"F": 0, "G": 1, "H": 2, "I": 3}
types = {"O": 0, "W": 1}
walls = [1, 2, 3, 4]
positions = {"U": 0, "L": 1}

# Define Z3 variables
painting_wall = [[Int("painting_wall[%s][%s]" % (s, t)) for t in types] for s in students]
painting_position = [[Int("painting_position[%s][%s]" % (s, t)) for t in types] for s in students]

solver = Solver()

# Constraint 1: Each student displays two paintings on different walls
for s in students:
    solver.add(painting_wall[students[s]][types["O"]] != painting_wall[students[s]][types["W"]])

# Constraint 2: Two paintings per wall, one upper, one lower, different students
for w in walls:
    solver.add(PbEq([(Or([And(painting_wall[students[s]][types[t]] == w, painting_position[students[s]][types[t]] == positions["U"]) for t in types]) for s in students], 1))
    solver.add(PbEq([(Or([And(painting_wall[students[s]][types[t]] == w, painting_position[students[s]][types[t]] == positions["L"]) for t in types]) for s in students], 1))


# Constraint 3: No wall has only watercolors
for w in walls:
    solver.add(Or([painting_wall[students[s]][types["O"]] == w for s in students]))

# Constraint 4: No wall has work of only one student
for w in walls:
  students_on_wall = [Or(painting_wall[students[s]][types["O"]] == w, painting_wall[students[s]][types["W"]] == w) for s in students]
  solver.add(PbGe([(s,1) for s in students_on_wall], 2))


# Constraint 5: No Franz and Isaacs on same wall
for w in walls:
    solver.add(Not(And(Or(painting_wall[students["F"]][types["O"]] == w, painting_wall[students["F"]][types["W"]] == w),
                       Or(painting_wall[students["I"]][types["O"]] == w, painting_wall[students["I"]][types["W"]] == w))))

# Constraint 6: Greene's watercolor with Franz's oil, Greene's watercolor is upper
solver.add(painting_wall[students["G"]][types["W"]] == painting_wall[students["F"]][types["O"]])
solver.add(painting_position[students["G"]][types["W"]] == positions["U"])

# Constraint 7: Isaacs's oil on wall 4 lower
solver.add(painting_wall[students["I"]][types["O"]] == 4)
solver.add(painting_position[students["I"]][types["O"]] == positions["L"])

# Check answer choices
choices = [
    painting_wall[students["F"]][types["W"]] == painting_wall[students["G"]][types["O"]],
    painting_wall[students["F"]][types["W"]] == painting_wall[students["H"]][types["O"]],
    painting_position[students["G"]][types["O"]] == positions["U"],
    painting_position[students["H"]][types["W"]] == positions["L"],
    painting_wall[students["I"]][types["W"]] == painting_wall[students["H"]][types["O"]]
]

for i, choice in enumerate(choices):
    solver.push()
    solver.add(choice)
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
