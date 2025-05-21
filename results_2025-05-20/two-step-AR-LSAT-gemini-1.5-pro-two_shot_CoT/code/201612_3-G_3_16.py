from z3 import *

# Define variables
painting_at = Array('painting_at', IntSort(), IntSort())
student_of_painting = [0, 0, 1, 1, 2, 2, 3, 3]
type_of_painting = [0, 1, 0, 1, 0, 1, 0, 1]
solver = Solver()

# Constraint 0 (All paintings distinct and in range)
solver.add(Distinct([painting_at[w] for w in range(8)]))
solver.add(And([And(painting_at[i] >= 0, painting_at[i] <= 7) for i in range(8)]))

# Constraint 4 (No wall has only watercolors)
solver.add(And([Or(type_of_painting[painting_at[w*2]] == 1, type_of_painting[painting_at[w*2+1]] == 1) for w in range(4)]))

# Constraint 5 (No wall has work of only one student)
solver.add(And([student_of_painting[painting_at[w*2]] != student_of_painting[painting_at[w*2+1]] for w in range(4)]))

# Constraint 6 (No wall has both Franz and Isaacs)
solver.add(And([Not(And(Or(student_of_painting[painting_at[w*2]] == 0, student_of_painting[painting_at[w*2+1]] == 0), Or(student_of_painting[painting_at[w*2]] == 3, student_of_painting[painting_at[w*2+1]] == 3))) for w in range(4)]))

# Constraint 7 (Greene's watercolor is above Franz's oil)
for w in range(4):
    # Corrected the implication and the condition for Franz's oil
    solver.add(Implies(And(Or(painting_at[w*2] == 2, painting_at[w*2+1] == 2), type_of_painting[2] == 1), # Greene's watercolor
                       And(Or(painting_at[w*2] == 1, painting_at[w*2+1] == 1), painting_at[w*2] == 1))) # Franz's oil above


# Constraint 8 (Isaacs's oil is on wall 4, lower)
solver.add(painting_at[7] == 7)

# Constraint 9 (Franz's oil is on wall 1)
solver.add(Or(painting_at[0] == 1, painting_at[1] == 1))

# Check answer choices
answer_choices = [
    Or(painting_at[6] == 1, painting_at[7] == 1),  # A
    Or(painting_at[2] == 2, painting_at[3] == 2),  # B
    Or(painting_at[2] == 3, painting_at[3] == 3),  # C
    Or(painting_at[4] == 5, painting_at[5] == 5),  # D
    Or(painting_at[0] == 6, painting_at[1] == 6)   # E
]

for i, choice in enumerate(answer_choices):
    solver.push()
    solver.add(choice)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()

```