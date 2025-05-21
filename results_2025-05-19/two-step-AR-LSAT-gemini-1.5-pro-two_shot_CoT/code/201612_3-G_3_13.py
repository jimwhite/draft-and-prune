from z3 import *

# Variables
student_wall_pos_painting = BoolVector('student_wall_pos_painting', 4 * 4 * 2 * 2)

solver = Solver()

# Helper function to access the boolean variable
def get_var(s, w, p, pt):
    return student_wall_pos_painting[s * 32 + w * 8 + p * 4 + pt * 2]

# Constraint 1: Each student displays exactly two paintings
for s in range(4):
    solver.add(Sum([If(get_var(s, w, p, pt), 1, 0) for w in range(4) for p in range(2) for pt in range(2)]) == 2)

# Constraint 2: Exactly two paintings on each wall
for w in range(4):
    solver.add(Sum([If(get_var(s, w, p, pt), 1, 0) for s in range(4) for p in range(2) for pt in range(2)]) == 2)

# Constraint 3: One painting in each position on each wall
for w in range(4):
    for p in range(2):
        solver.add(Sum([If(get_var(s, w, p, pt), 1, 0) for s in range(4) for pt in range(2)]) == 1)

# Constraint 4: Each student displays one oil and one watercolor
for s in range(4):
    for pt in range(2):
        solver.add(Sum([If(get_var(s, w, p, pt), 1, 0) for w in range(4) for p in range(2)]) == 1)

# Constraint 5: No wall has only watercolors
for w in range(4):
    solver.add(Or([get_var(s, w, p, 0) for s in range(4) for p in range(2)]))

# Constraint 6: No wall has work of only one student
for w in range(4):
    for s1 in range(4):
        for s2 in range(s1 + 1, 4):
            solver.add(Or(Not(Or([get_var(s1, w, p, pt) for p in range(2) for pt in range(2)])), Not(Or([get_var(s2, w, p, pt) for p in range(2) for pt in range(2)]))))

# Constraint 7: No wall has both Franz and Isaacs
for w in range(4):
    solver.add(Not(And(Or([get_var(0, w, p, pt) for p in range(2) for pt in range(2)]), Or([get_var(3, w, p, pt) for p in range(2) for pt in range(2)]))))

# Constraint 8: Greene's watercolor with Franz's oil
for w in range(4):
    for p in range(2):
        solver.add(Implies(get_var(1, w, p, 1), get_var(0, w, p, 0)))

# Constraint 9: Isaacs's oil on wall 4 lower
solver.add(get_var(3, 3, 1, 0))

# Constraint 10: Isaacs's watercolor on wall 2
solver.add(Or(get_var(3, 1, 0, 1), get_var(3, 1, 1, 1)))

# Constraint 11: Franz's oil on wall 3
solver.add(Or(get_var(0, 2, 0, 0), get_var(0, 2, 1, 0)))

# Answer choices
options = [
    [0, 0, 1],  # Franz's watercolor on wall 1
    [1, 0, 0],  # Greene's oil on wall 1
    [1, 0, 1],  # Greene's watercolor on wall 1
    [2, 0, 0],  # Hidalgo's oil on wall 1
    [2, 0, 1]   # Hidalgo's watercolor on wall 1
]

for i, (s, w, pt) in enumerate(options):
    solver.push()
    solver.add(Not(Or(get_var(s, w, 0, pt), get_var(s, w, 1, pt))))
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
