from z3 import *

# Variables
pianist = Array('pianist', IntSort(), IntSort())
piece_type = Array('piece_type', IntSort(), IntSort())
wayne_modern_before_i = Array('wayne_modern_before_i', IntSort(), BoolSort())

solver = Solver()

# Constraints
for i in range(5):
    solver.add(Or(pianist[i] == 0, pianist[i] == 1))
    solver.add(Or(piece_type[i] == 0, piece_type[i] == 1))

solver.add(piece_type[2] == 1)

solver.add(Sum([If(And(piece_type[i] == 1, piece_type[i+1] == 1), 1, 0) for i in range(4)]) == 1)

solver.add(Or(And(pianist[3] == 0, piece_type[3] == 1), And(pianist[3] == 1, piece_type[3] == 0)))

solver.add(pianist[1] != pianist[4])

solver.add(wayne_modern_before_i[0] == False)
for i in range(1, 5):
    solver.add(wayne_modern_before_i[i] == Or(wayne_modern_before_i[i-1], And(pianist[i-1] == 0, piece_type[i-1] == 0)))

for i in range(5):
    solver.add(Implies(piece_type[i] == 1, wayne_modern_before_i[i]))

# Question Constraint
solver.add(pianist[0] == pianist[1])

# Answer Choices
choices = [
    (pianist[0] == 1, 'A'),
    (pianist[2] == 0, 'B'),
    (pianist[4] == 1, 'C'),
    (piece_type[1] == 1, 'D'),
    (piece_type[3] == 0, 'E')
]

for choice, option in choices:
    solver.push()
    solver.add(Not(choice))
    if solver.check() == unsat:
        print(f"Option {option} is correct")
        exit()
    solver.pop()