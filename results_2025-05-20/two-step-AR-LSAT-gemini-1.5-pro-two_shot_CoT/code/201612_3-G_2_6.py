from z3 import *

clue_in_chapter = Array('clue_in_chapter', IntSort(), IntSort())
i = Int('i')
solver = Solver()

# Clue Mappings: R=0, S=1, T=2, U=3, W=4, X=5, Z=6

# Constraint 0 (Domain)
solver.add(ForAll([i], Implies(And(i >= 0, i <= 6), And(clue_in_chapter[i] >= 0, clue_in_chapter[i] <= 6))))

# Constraint 1 (Distinctness)
solver.add(Distinct([clue_in_chapter[i] for i in range(7)]))

# Constraint 2 (T not in Chapter 1)
solver.add(clue_in_chapter[0] != 2)

# Constraint 3 (T before W, two chapters apart)
solver.add(Exists([i], And(clue_in_chapter[i] == 2, clue_in_chapter[i+3] == 4, i >= 0, i <= 3)))

# Constraint 4 (S and Z not adjacent)
solver.add(ForAll([i], Implies(And(i >= 0, i <= 5), Not(Or(And(clue_in_chapter[i] == 1, clue_in_chapter[i+1] == 6), And(clue_in_chapter[i] == 6, clue_in_chapter[i+1] == 1))))))

# Constraint 5 (W and X not adjacent)
solver.add(ForAll([i], Implies(And(i >= 0, i <= 5), Not(Or(And(clue_in_chapter[i] == 4, clue_in_chapter[i+1] == 5), And(clue_in_chapter[i] == 5, clue_in_chapter[i+1] == 4))))))

# Constraint 6 (U and X adjacent)
solver.add(Exists([i], Or(And(clue_in_chapter[i] == 3, clue_in_chapter[i+1] == 5, i >= 0, i <= 5), And(clue_in_chapter[i] == 5, clue_in_chapter[i+1] == 3, i >= 0, i <= 5))))

answer_choices = [
    [1, 2, 6, 5, 3, 4, 0],  # S, T, Z, X, U, W, R
    [2, 5, 3, 4, 1, 0, 6],  # T, X, U, W, S, R, Z
    [3, 1, 5, 2, 6, 0, 4],  # U, S, X, T, Z, R, W
    [5, 3, 2, 6, 0, 4, 1],  # X, U, T, Z, R, W, S
    [6, 0, 2, 3, 5, 4, 1]   # Z, R, T, U, X, W, S
]

for option_index, choice in enumerate(answer_choices):
    solver.push()
    for chapter_index, clue_index in enumerate(choice):
        solver.add(clue_in_chapter[chapter_index] == clue_index)
    if solver.check() == sat:
        print(f"Option {chr(65 + option_index)} is correct")
        exit()
    solver.pop()