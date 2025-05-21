from z3 import *

clue_in_chapter = Array('clue_in_chapter', IntSort(), IntSort())
solver = Solver()

# Constraint 0 (Domain)
for i in range(7):
    solver.add(And(clue_in_chapter[i] >= 0, clue_in_chapter[i] <= 6))

# Constraint 1 (Distinctness)
solver.add(Distinct([clue_in_chapter[i] for i in range(7)]))

# Constraint 2 (T not in Chapter 1)
solver.add(clue_in_chapter[0] != 2)

# Constraint 3 (T before W, two chapters apart)
solver.add(Or([And(clue_in_chapter[i] == 2, clue_in_chapter[i+3] == 4) for i in range(4)]))

# Constraint 4 (S and Z not adjacent)
for i in range(6):
    solver.add(Not(Or(And(clue_in_chapter[i] == 1, clue_in_chapter[i+1] == 6), And(clue_in_chapter[i] == 6, clue_in_chapter[i+1] == 1))))

# Constraint 5 (W and X not adjacent)
for i in range(6):
    solver.add(Not(Or(And(clue_in_chapter[i] == 4, clue_in_chapter[i+1] == 5), And(clue_in_chapter[i] == 5, clue_in_chapter[i+1] == 4))))

# Constraint 6 (U and X adjacent)
solver.add(Or([Or(And(clue_in_chapter[i] == 3, clue_in_chapter[i+1] == 5), And(clue_in_chapter[i] == 5, clue_in_chapter[i+1] == 3)) for i in range(6)]))

# Constraint 7 (U in Chapter 3)
solver.add(clue_in_chapter[2] == 3)

# Check answer choices
answer_choices = [
    (0, 0),  # R in chapter 1
    (4, 0),  # R in chapter 5
    (6, 1),  # S in chapter 7
    (5, 4),  # W in chapter 6
    (3, 5)   # X in chapter 4
]

for i, (chapter, clue) in enumerate(answer_choices):
    solver.push()
    solver.add(clue_in_chapter[chapter] == clue)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()