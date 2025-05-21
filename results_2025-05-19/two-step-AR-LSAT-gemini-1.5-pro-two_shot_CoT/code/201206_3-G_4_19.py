from z3 import *

# Variables
pianist = Array('pianist', IntSort(), IntSort())
piece_type = Array('piece_type', IntSort(), IntSort())
i = Int('i')
j = Int('j')

solver = Solver()

# Constraints
solver.add(ForAll(i, Implies(And(i >= 0, i < 5), And(pianist[i] >= 0, pianist[i] <= 1))))
solver.add(ForAll(i, Implies(And(i >= 0, i < 5), And(piece_type[i] >= 0, piece_type[i] <= 1))))
solver.add(piece_type[2] == 1)
solver.add(Or(And(piece_type[0] == 1, piece_type[1] == 1), And(piece_type[1] == 1, piece_type[2] == 1), And(piece_type[2] == 1, piece_type[3] == 1), And(piece_type[3] == 1, piece_type[4] == 1)))
solver.add(Or(And(pianist[3] == 0, piece_type[3] == 1), And(pianist[3] == 1, piece_type[3] == 0)))
solver.add(pianist[1] != pianist[4])
solver.add(ForAll(i, Implies(And(i >= 0, i < 5), Implies(piece_type[i] == 1, Exists(j, Implies(And(j >= 0, j <= i), And(pianist[j] == 0, piece_type[j] == 0)))))))


# Check answer choices
for n, option in enumerate(["zero", "one", "two", "three", "four"]):
    solver.push()
    solver.add(Sum([If(And(pianist[k] == 0, piece_type[k] == 1), 1, 0) for k in range(5)]) == n)
    if solver.check() == sat:
        print(f"Option {chr(65 + n)} is correct")
        exit()
    solver.pop()