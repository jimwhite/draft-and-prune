from z3 import *

clue_in_chapter = Array('clue_in_chapter', IntSort(), IntSort())
solver = Solver()

# Constraint 0 (Domain)
i = Int('i')
solver.add(ForAll([i], Implies(And(i >= 0, i < 7), And(clue_in_chapter[i] >= 0, clue_in_chapter[i] < 7))))

# Constraint 1 (Distinctness)
solver.add(Distinct([clue_in_chapter[i] for i in range(7)]))

# Constraint 2 (T not in Chapter 1)
solver.add(clue_in_chapter[0] != 2)

# Constraint 3 (T before W, two chapters apart)
c = Int('c')
solver.add(ForAll([c], Implies(And(c >= 0, c < 5, clue_in_chapter[c] == 2), clue_in_chapter[c + 3] == 4)))

# Constraint 4 (S and Z not adjacent)
c = Int('c')
solver.add(ForAll([c], Implies(And(c >= 0, c < 6), Or(clue_in_chapter[c] != 1, clue_in_chapter[c + 1] != 6))))

# Constraint 5 (W and X not adjacent)
c = Int('c')
solver.add(ForAll([c], Implies(And(c >= 0, c < 6), Or(clue_in_chapter[c] != 4, clue_in_chapter[c + 1] != 5))))

# Constraint 6 (U and X adjacent)
c = Int('c')
solver.add(ForAll([c], Implies(And(c >= 0, c < 6), Or(
    And(clue_in_chapter[c] == 3, clue_in_chapter[c + 1] == 5),
    And(clue_in_chapter[c] == 5, clue_in_chapter[c + 1] == 3)))))


# Constraint 7 (X in Chapter 1)
solver.add(clue_in_chapter[0] == 5)

# Check answer choices
answer_choices = [
    (2, 0),  # A: R in chapter 3
    (6, 0),  # B: R in chapter 7
    (1, 1),  # C: S in chapter 2
    (4, 4),  # D: W in chapter 5
    (2, 6)   # E: Z in chapter 3
]

for option, (chapter, clue) in enumerate(answer_choices):
    solver.push()
    solver.add(clue_in_chapter[chapter] == clue)
    if solver.check() == sat:
        print(f"Option {chr(65 + option)} is correct")
        exit()
    solver.pop()