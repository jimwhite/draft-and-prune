from z3 import *

# Variables
pianist = Array('pianist', IntSort(), IntSort())
piece_type = Array('piece_type', IntSort(), IntSort())
solver = Solver()
i = Int('i')
j = Int('j')

# Constraints
solver.add(ForAll(i, Implies(And(i >= 0, i < 5), And(pianist[i] >= 0, pianist[i] <= 1))))
solver.add(ForAll(i, Implies(And(i >= 0, i < 5), And(piece_type[i] >= 0, piece_type[i] <= 1))))
solver.add(piece_type[2] == 1)
solver.add(Or(And(piece_type[0] == 1, piece_type[1] == 1, piece_type[2] == 0, piece_type[3] == 0, piece_type[4] == 0),
             And(piece_type[1] == 1, piece_type[2] == 1, piece_type[0] == 0, piece_type[3] == 0, piece_type[4] == 0),
             And(piece_type[2] == 1, piece_type[3] == 1, piece_type[0] == 0, piece_type[1] == 0, piece_type[4] == 0),
             And(piece_type[3] == 1, piece_type[4] == 1, piece_type[0] == 0, piece_type[1] == 0, piece_type[2] == 0)))
solver.add(Or(And(pianist[3] == 0, piece_type[3] == 1), And(pianist[3] == 1, piece_type[3] == 0)))
solver.add(pianist[1] != pianist[4])
solver.add(ForAll([i], Implies(And(i >= 0, i < 5, piece_type[i] == 1), Exists([j], And(j >= 0, j <= i, pianist[j] == 0, piece_type[j] == 0)))))


# Question Constraint
solver.add(And(pianist[4] == 0, piece_type[4] == 1))

# Answer Choices
options = [
    (pianist[0] == 1),  # Zara performs the first solo
    (pianist[1] == 0),  # Wayne performs the second solo
    (pianist[2] == 1),  # Zara performs the third solo
    (piece_type[1] == 0),  # The second solo is a modern piece
    (piece_type[3] == 1)  # The fourth solo is a traditional piece
]

for i in range(len(options)):
    solver.push()
    solver.add(options[i])
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()