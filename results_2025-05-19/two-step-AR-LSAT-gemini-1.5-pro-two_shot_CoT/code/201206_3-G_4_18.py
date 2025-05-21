from z3 import *

# Variables
pianist = Array('pianist', IntSort(), IntSort())
piece_type = Array('piece_type', IntSort(), IntSort())
i = Int('i')
j = Int('j')

solver = Solver()

# Constraint 1: Pianist Domain
solver.add(ForAll(i, Implies(And(i >= 0, i < 5), Or(pianist[i] == 0, pianist[i] == 1))))

# Constraint 2: Piece Type Domain
solver.add(ForAll(i, Implies(And(i >= 0, i < 5), Or(piece_type[i] == 0, piece_type[i] == 1))))

# Constraint 3: Third Solo Traditional
solver.add(piece_type[2] == 1)

# Constraint 4: Exactly Two Consecutive Traditional
solver.add(Or(And(piece_type[0] == 1, piece_type[1] == 1),
             And(piece_type[1] == 1, piece_type[2] == 1),
             And(piece_type[2] == 1, piece_type[3] == 1),
             And(piece_type[3] == 1, piece_type[4] == 1)))

# Constraint 5: Fourth Solo
solver.add(Or(And(pianist[3] == 0, piece_type[3] == 1), And(pianist[3] == 1, piece_type[3] == 0)))

# Constraint 6: Second and Fifth Solo Pianists Different
solver.add(pianist[1] != pianist[4])

# Constraint 7: No Traditional Until Wayne Modern
solver.add(ForAll(i, Implies(And(i >= 0, i < 5, piece_type[i] == 1), Exists(j, And(j >= 0, j < 5, j <= i, pianist[j] == 0, piece_type[j] == 0)))))

# Answer Choices
options = [
    [0, 2, 3],  # A
    [1, 2, 3],  # B
    [2, 3],  # C
    [2, 4],  # D
    [3, 4]  # E
]

for option_index, option in enumerate(options):
    solver.push()
    for i in range(5):
        if i in option:
            solver.add(piece_type[i] == 1)
        else:
            solver.add(piece_type[i] == 0)
    if solver.check() == sat:
        print(f"Option {chr(65 + option_index)} is correct")
        exit()
    solver.pop()