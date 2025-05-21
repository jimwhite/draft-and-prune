from z3 import *

solver = Solver()

clue_in_chapter = Array('clue_in_chapter', IntSort(), IntSort())

# Constraint 0 (Domain)
i = Int('i')
solver.add(ForAll([i], Implies(And(i >= 0, i <= 6), And(clue_in_chapter[i] >= 0, clue_in_chapter[i] <= 6))))

# Constraint 1 (Distinctness)
solver.add(Distinct([clue_in_chapter[i] for i in range(7)]))

# Constraint 2 (T not in Chapter 1)
solver.add(clue_in_chapter[0] != 2)

# Constraint 3 (T before W, two chapters apart)
i = Int('i')
solver.add(Exists([i], And(clue_in_chapter[i] == 2, clue_in_chapter[i+3] == 4, i >= 0, i <= 4)))

# Constraint 4 (S and Z not adjacent)
i = Int('i')
solver.add(ForAll([i], Implies(And(i >= 0, i < 6), Implies(clue_in_chapter[i] == 1, clue_in_chapter[i+1] != 6))))
solver.add(ForAll([i], Implies(And(i > 0, i <= 6), Implies(clue_in_chapter[i] == 1, clue_in_chapter[i-1] != 6))))


# Constraint 5 (W and X not adjacent)
i = Int('i')
solver.add(ForAll([i], Implies(And(i >= 0, i < 6), Implies(clue_in_chapter[i] == 4, clue_in_chapter[i+1] != 5))))
solver.add(ForAll([i], Implies(And(i > 0, i <= 6), Implies(clue_in_chapter[i] == 4, clue_in_chapter[i-1] != 5))))

# Constraint 6 (U and X adjacent)
i = Int('i')
solver.add(Exists([i], And(i >= 0, i < 6, Or(And(clue_in_chapter[i] == 3, clue_in_chapter[i+1] == 5), And(clue_in_chapter[i] == 5, clue_in_chapter[i+1] == 3)))))

# U in Chapter 3
solver.add(clue_in_chapter[2] == 3)

# Check answer choices
answer_choices = [
    (0, 0),  # R in Chapter 1
    (4, 0),  # R in Chapter 5
    (6, 1),  # S in Chapter 7
    (5, 4),  # W in Chapter 6
    (3, 5)   # X in Chapter 4
]

for choice, (chapter, clue) in enumerate(answer_choices):
    solver.push()
    solver.add(clue_in_chapter[chapter] == clue)
    if solver.check() == sat:
        print(f"Option {chr(65 + choice)} is correct")
        exit()
    solver.pop()