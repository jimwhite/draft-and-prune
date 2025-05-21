from z3 import *

clue_in_chapter = Array('clue_in_chapter', IntSort(), IntSort())
solver = Solver()

# Constraint 0 (Domain)
i = Int('i')
solver.add(ForAll([i], Implies(And(i >= 0, i < 7), And(clue_in_chapter[i] >= 0, clue_in_chapter[i] < 7))))

# Constraint 1 (Distinctness)
solver.add(Distinct([clue_in_chapter[i] for i in range(7)]))

# Constraint 2 (T before W, two chapters apart)
i = Int('i')
solver.add(ForAll([i], Implies(And(i >= 0, i < 5), Implies(clue_in_chapter[i] == 2, clue_in_chapter[i + 2] == 4))))

# Constraint 3 (S and Z not adjacent)
i = Int('i')
solver.add(ForAll([i], Implies(And(i >= 0, i < 7), Implies(clue_in_chapter[i] == 1,
                                                               And(If(i < 6, clue_in_chapter[i + 1] != 6, True),
                                                                   If(i > 0, clue_in_chapter[i - 1] != 6, True))))))

# Constraint 4 (W and X not adjacent)
i = Int('i')
solver.add(ForAll([i], Implies(And(i >= 0, i < 7), Implies(clue_in_chapter[i] == 4,
                                                               And(If(i < 6, clue_in_chapter[i + 1] != 5, True),
                                                                   If(i > 0, clue_in_chapter[i - 1] != 5, True))))))

# Constraint 5 (U and X adjacent)
i = Int('i')
solver.add(ForAll([i], Implies(And(i >= 0, i < 7), Implies(clue_in_chapter[i] == 3,
                                                               Or(If(i < 6, clue_in_chapter[i + 1] == 5, False),
                                                                  If(i > 0, clue_in_chapter[i - 1] == 5, False))))))

# Constraint 6 (T not in Chapter 1)
constraint_6 = clue_in_chapter[0] != 2

options = [
    clue_in_chapter[1] != 3,  # A
    clue_in_chapter[3] != 4,  # B
    clue_in_chapter[5] != 5,  # C
    ForAll([i, j], Implies(And(i >= 0, i < 7, j >= 0, j < 7, clue_in_chapter[i] == 3, clue_in_chapter[j] == 2), i < j)),  # D
    ForAll([i, j], Implies(And(i >= 0, i < 7, j >= 0, j < 7, clue_in_chapter[i] == 5, clue_in_chapter[j] == 4), i < j))  # E
]

for opt_index, option in enumerate(options):
    solver.push()
    solver.add(option)
    solver.add(constraint_6)
    result1 = solver.check()
    solver.pop()

    solver.push()
    solver.add(option)
    result2 = solver.check()
    solver.pop()

    if result1 == result2:
        print(f"Option {chr(65 + opt_index)} is correct")
        exit()
