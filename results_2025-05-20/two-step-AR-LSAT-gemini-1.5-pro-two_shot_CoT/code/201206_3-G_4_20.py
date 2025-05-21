from z3 import *

# Variables
pianist = Array('pianist', IntSort(), IntSort())
piece_type = Array('piece_type', IntSort(), IntSort())
wayne_modern_before = Array('wayne_modern_before', IntSort(), BoolSort())

solver = Solver()

# Constraint 1: Pianist Domain
for i in range(5):
    solver.add(And(pianist[i] >= 0, pianist[i] <= 1))

# Constraint 2: Piece Type Domain
for i in range(5):
    solver.add(And(piece_type[i] >= 0, piece_type[i] <= 1))

# Revised Constraint 3: Piece Types
solver.add(Or(
    And(piece_type[0] == 0, piece_type[1] == 1, piece_type[2] == 1, piece_type[3] == 0, piece_type[4] == 0),
    And(piece_type[0] == 0, piece_type[1] == 0, piece_type[2] == 1, piece_type[3] == 1, piece_type[4] == 0)
))


# Constraint 6: Fourth Solo
solver.add(Or(And(pianist[3] == 0, piece_type[3] == 1), And(pianist[3] == 1, piece_type[3] == 0)))

# Constraint 7: Second and Fifth Solo
solver.add(pianist[1] != pianist[4])

# Constraint 8: No Traditional Until Wayne Modern
solver.add(wayne_modern_before[0] == False)
for i in range(4):
    solver.add(Implies(And(pianist[i] == 0, piece_type[i] == 0), wayne_modern_before[i+1] == True))
    solver.add(Implies(Not(And(pianist[i] == 0, piece_type[i] == 0)), wayne_modern_before[i+1] == wayne_modern_before[i]))
for i in range(5):
    solver.add(Implies(piece_type[i] == 1, wayne_modern_before[i] == True))

# Constraint 9: First and Second Solo Pianist Same
solver.add(pianist[0] == pianist[1])

# Answer Choices and their negations
answer_choices = [
    (pianist[0] != 1),  # Zara performs the first solo (negation: Wayne performs the first solo)
    (pianist[2] != 0),  # Wayne performs the third solo (negation: Zara performs the third solo)
    (pianist[4] != 1),  # Zara performs the fifth solo (negation: Wayne performs the fifth solo)
    (piece_type[1] != 1),  # The second solo is a traditional piece (negation: The second solo is a modern piece)
    (piece_type[3] != 0)   # The fourth solo is a modern piece (negation: The fourth solo is a traditional piece)
]

for i, negation in enumerate(answer_choices):
    solver.push()
    solver.add(negation)
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()