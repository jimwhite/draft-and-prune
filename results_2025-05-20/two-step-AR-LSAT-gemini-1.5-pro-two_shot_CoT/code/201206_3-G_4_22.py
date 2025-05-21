from z3 import *

# Variables
pianist = Array('pianist', IntSort(), IntSort())
piece_type = Array('piece_type', IntSort(), IntSort())
i = Int('i')

# Solver
solver = Solver()

# Constraints
# Constraint 1 (Pianist Domain)
solver.add(ForAll(i, Implies(And(i >= 0, i < 5), Or(pianist[i] == 0, pianist[i] == 1))))

# Constraint 2 (Piece Type Domain)
solver.add(ForAll(i, Implies(And(i >= 0, i < 5), Or(piece_type[i] == 0, piece_type[i] == 1))))

# Constraint 3 (Third Solo Traditional)
solver.add(piece_type[2] == 1)

# Constraint 4 (Exactly Two Consecutive Traditional)
solver.add(Or(
    And(piece_type[0] == 0, piece_type[1] == 1, piece_type[2] == 1, piece_type[3] == 0, piece_type[4] == 0),
    And(piece_type[0] == 0, piece_type[1] == 0, piece_type[2] == 1, piece_type[3] == 1, piece_type[4] == 0)
))

# Constraint 5 (Fourth Solo)
solver.add(Or(And(pianist[3] == 0, piece_type[3] == 1), And(pianist[3] == 1, piece_type[3] == 0)))

# Constraint 6 (Second and Fifth Solo Pianists Different)
solver.add(pianist[1] != pianist[4])


# Constraint 7 (No Traditional Until Wayne Modern)
solver.add(piece_type[0] == 0)
solver.add(Implies(piece_type[1] == 1, Or(And(pianist[0] == 0, piece_type[0] == 0),And(pianist[1] == 0, piece_type[1] == 0))))
solver.add(Implies(piece_type[2] == 1, Or(And(pianist[0] == 0, piece_type[0] == 0), And(pianist[1] == 0, piece_type[1] == 0), And(pianist[2] == 0, piece_type[2] == 0))))
solver.add(Implies(piece_type[3] == 1, Or(And(pianist[0] == 0, piece_type[0] == 0), And(pianist[1] == 0, piece_type[1] == 0), And(pianist[2] == 0, piece_type[2] == 0), And(pianist[3] == 0, piece_type[3] == 0))))
solver.add(Implies(piece_type[4] == 1, Or(And(pianist[0] == 0, piece_type[0] == 0), And(pianist[1] == 0, piece_type[1] == 0), And(pianist[2] == 0, piece_type[2] == 0), And(pianist[3] == 0, piece_type[3] == 0), And(pianist[4] == 0, piece_type[4] == 0))))



# Question Premise
solver.add(And(pianist[4] == 0, piece_type[4] == 1))

# Answer Choices
options = [
    pianist[0] == 1,  # A
    pianist[1] == 0,  # B
    pianist[2] == 1,  # C
    piece_type[1] == 0,  # D
    piece_type[3] == 1  # E
]

for i, option in enumerate(options):
    solver.push()
    solver.add(option)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()