from z3 import *

# Entities (as IDs)
Franz, Greene, Hidalgo, Isaacs = 0, 1, 2, 3
Oil, Watercolor = 0, 1

# Variables
student_at = [[Int(f"student_at[{w}][{p}]") for p in range(2)] for w in range(4)]
painting_type_at = [[Int(f"painting_type_at[{w}][{p}]") for p in range(2)] for w in range(4)]

solver = Solver()

# Domain Constraints
for w in range(4):
    for p in range(2):
        solver.add(student_at[w][p] >= 0, student_at[w][p] < 4)
        solver.add(painting_type_at[w][p] >= 0, painting_type_at[w][p] < 2)


# Uniqueness Constraint
for w1 in range(4):
    for p1 in range(2):
        for w2 in range(4):
            for p2 in range(2):
                if w1 != w2 or p1 != p2:
                    solver.add(Or(student_at[w1][p1] != student_at[w2][p2], painting_type_at[w1][p1] != painting_type_at[w2][p2]))

# Constraint 4: No wall has only watercolors
for w in range(4):
    solver.add(Or(painting_type_at[w][0] == Oil, painting_type_at[w][1] == Oil))

# Constraint 5: No wall has work of only one student
for w in range(4):
    solver.add(student_at[w][0] != student_at[w][1])

# Constraint 6: No wall has both Franz and Isaacs
for w in range(4):
    solver.add(Not(Or(And(student_at[w][0] == Franz, student_at[w][1] == Isaacs), And(student_at[w][0] == Isaacs, student_at[w][1] == Franz))))

# Constraint 7: Greene's watercolor above Franz's oil
solver.add(Or([And(student_at[w][0] == Greene, painting_type_at[w][0] == Watercolor, student_at[w][1] == Franz, painting_type_at[w][1] == Oil) for w in range(4)]))

# Constraint 8: Isaacs's oil on wall 4, lower
solver.add(And(student_at[3][1] == Isaacs, painting_type_at[3][1] == Oil))

# Answer Choices
choices = [
    [(Franz, Oil), (Franz, Watercolor), (Greene, Oil), (Isaacs, Oil)],
    [(Franz, Oil), (Hidalgo, Watercolor), (Isaacs, Watercolor), (Isaacs, Oil)],
    [(Greene, Oil), (Franz, Oil), (Isaacs, Oil), (Hidalgo, Oil)],
    [(Hidalgo, Oil), (Greene, Oil), (Greene, Watercolor), (Isaacs, Oil)],
    [(Hidalgo, Watercolor), (Franz, Oil), (Greene, Oil), (Isaacs, Oil)]
]

for i, choice in enumerate(choices):
    solver.push()
    for wall_idx, (student, painting_type) in enumerate(choice):
        solver.add(student_at[wall_idx][1] == student)
        solver.add(painting_type_at[wall_idx][1] == painting_type)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
