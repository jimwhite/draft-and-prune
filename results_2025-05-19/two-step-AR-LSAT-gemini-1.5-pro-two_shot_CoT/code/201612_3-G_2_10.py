from z3 import *

clue_in_chapter = Array('clue_in_chapter', IntSort(), IntSort())
solver = Solver()

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
solver.add(ForAll([i], Implies(And(i >= 0, i < 6), Not(Or(And(clue_in_chapter[i] == 1, clue_in_chapter[i+1] == 6), And(clue_in_chapter[i] == 6, clue_in_chapter[i+1] == 1))))))

# Constraint 5 (W and X not adjacent)
i = Int('i')
solver.add(ForAll([i], Implies(And(i >= 0, i < 6), Not(Or(And(clue_in_chapter[i] == 4, clue_in_chapter[i+1] == 5), And(clue_in_chapter[i] == 5, clue_in_chapter[i+1] == 4))))))

# Constraint 6 (U and X adjacent)
i = Int('i')
solver.add(Exists([i], And(Or(And(clue_in_chapter[i] == 3, clue_in_chapter[i+1] == 5), And(clue_in_chapter[i] == 5, clue_in_chapter[i+1] == 3)), i >= 0, i <= 5)))

# Check answer choices
answers = [
    (0, clue_in_chapter[6] == 0),  # A: R in chapter 7
    (1, clue_in_chapter[4] == 2),  # B: T in chapter 5
    (2, clue_in_chapter[6] == 3),  # C: U in chapter 7
    (3, clue_in_chapter[2] == 4),  # D: W in chapter 3
    (4, clue_in_chapter[5] == 5)   # E: X in chapter 6
]

for i, constraint in answers:
    solver.push()
    solver.add(constraint)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()