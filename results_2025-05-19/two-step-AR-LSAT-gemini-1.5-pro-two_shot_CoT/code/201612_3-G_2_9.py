from z3 import *

clue_in_chapter = Array('clue_in_chapter', IntSort(), IntSort())
solver = Solver()

# Constraint 0 (Domain)
i = Int('i')
solver.add(ForAll(i, Implies(And(i >= 0, i <= 6), And(clue_in_chapter[i] >= 0, clue_in_chapter[i] <= 6))))

# Constraint 1 (Distinctness)
solver.add(Distinct([clue_in_chapter[i] for i in range(7)]))

# Constraint 2 (T not in Chapter 1)
solver.add(clue_in_chapter[0] != 2)

# Constraint 4 (S and Z not adjacent)
for i in range(7):
    solver.add(Implies(clue_in_chapter[i] == 1, And(If(i > 0, clue_in_chapter[i-1] != 6, True), If(i < 6, clue_in_chapter[i+1] != 6, True))))

# Constraint 5 (W and X not adjacent)
for i in range(7):
    solver.add(Implies(clue_in_chapter[i] == 4, And(If(i > 0, clue_in_chapter[i-1] != 5, True), If(i < 6, clue_in_chapter[i+1] != 5, True))))

# Constraint 7 (Z in Chapter 7)
solver.add(clue_in_chapter[6] == 6)

# Answer Choices
answer_choices = [
    (2, 0),  # A: R in Chapter 3
    (2, 1),  # B: S in Chapter 3
    (3, 2),  # C: T in Chapter 4
    (0, 3),  # D: U in Chapter 1
    (4, 5)   # E: X in Chapter 5
]

for choice_index, (chapter, clue) in enumerate(answer_choices):
    solver.push()
    solver.add(clue_in_chapter[chapter] == clue)
    
    for i in range(5):  # Constraint 3 (T before W, two chapters apart)
        solver.push()
        solver.add(clue_in_chapter[i] == 2)
        solver.add(clue_in_chapter[i+3] == 4)
        
        for j in range(6): # Constraint 6 (U and X adjacent)
            solver.push()
            solver.add(Or(And(clue_in_chapter[j] == 3, clue_in_chapter[j+1] == 5), And(clue_in_chapter[j] == 5, clue_in_chapter[j+1] == 3)))
            if solver.check() == sat:
                print(f"Option {chr(65 + choice_index)} is correct")
                exit()
            solver.pop()
        solver.pop()
    solver.pop()