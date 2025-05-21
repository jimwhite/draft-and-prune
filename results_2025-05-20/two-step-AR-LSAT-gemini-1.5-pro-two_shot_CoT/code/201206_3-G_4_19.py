from z3 import *

# Variables
pianist = Array('pianist', IntSort(), IntSort())
piece_type = Array('piece_type', IntSort(), IntSort())
wayne_modern_before = Array('wayne_modern_before', IntSort(), BoolSort())

solver = Solver()

# Constraints
# Constraint 1 (Pianist Domain)
solver.add(ForAll([i], Implies(And(i >= 0, i < 5), Or(pianist[i] == 0, pianist[i] == 1))))

# Constraint 2 (Piece Type Domain)
solver.add(ForAll([i], Implies(And(i >= 0, i < 5), Or(piece_type[i] == 0, piece_type[i] == 1))))

# Constraint 3 (Third Solo Traditional)
solver.add(piece_type[2] == 1)

# Constraint 4 (Exactly Two Consecutive Traditional)
solver.add(Or(
    And(piece_type[0] == 0, piece_type[1] == 1, piece_type[2] == 1, piece_type[3] == 0, piece_type[4] == 0),
    And(piece_type[0] == 0, piece_type[1] == 0, piece_type[2] == 1, piece_type[3] == 1, piece_type[4] == 0)
))

# Constraint 5 (Fourth Solo)
solver.add(Or(And(pianist[3] == 0, piece_type[3] == 1), And(pianist[3] == 1, piece_type[3] == 0)))

# Constraint 6 (Second and Fifth Solo)
solver.add(pianist[1] != pianist[4])

# Constraint 7 (No Traditional Until Wayne Modern)
solver.add(wayne_modern_before[0] == False)
solver.add(ForAll([i], Implies(And(i > 0, i < 5),
                             wayne_modern_before[i] == Or(wayne_modern_before[i - 1],
                                                          And(pianist[i - 1] == 0, piece_type[i - 1] == 0)))))
solver.add(ForAll([i], Implies(piece_type[i] == 1, wayne_modern_before[i])))


# Answering the Question
for k in range(6):  # Iterate from 0 to 5
    solver.push()
    solver.add(Sum([If(And(pianist[i] == 0, piece_type[i] == 1), 1, 0) for i in range(5)]) == k)
    if solver.check() == sat:
        answers = ["zero", "one", "two", "three", "four", "five"]
        print(f"Option {'ABCDE'[k] if k < 5 else 'F'} is correct")  # Adjusted for potential k=5
        exit()
    solver.pop()

