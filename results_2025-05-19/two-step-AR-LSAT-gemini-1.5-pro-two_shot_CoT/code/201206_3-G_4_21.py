from z3 import *

# Variables
pianist = Array('pianist', IntSort(), IntSort())
piece_type = Array('piece_type', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints
i = Int('i')
solver.add(ForAll(i, Implies(And(i >= 0, i < 5), And(pianist[i] >= 0, pianist[i] <= 1))))  # Pianist Domain
solver.add(ForAll(i, Implies(And(i >= 0, i < 5), And(piece_type[i] >= 0, piece_type[i] <= 1))))  # Piece Type Domain
solver.add(piece_type[2] == 1)  # Third Solo Traditional
solver.add(Sum([If(And(piece_type[i] == 1, piece_type[i+1] == 1), 1, 0) for i in range(4)]) == 1)  # Exactly Two Consecutive Traditional
solver.add(Or(And(pianist[3] == 0, piece_type[3] == 1), And(pianist[3] == 1, piece_type[3] == 0)))  # Fourth Solo
solver.add(pianist[1] != pianist[4])  # Second and Fifth Solo Pianists Different

for k in range(5):
    solver.add(Implies(piece_type[k] == 1, Or([And(pianist[j] == 0, piece_type[j] == 0) for j in range(k+1)]))) # No Traditional Until Wayne Modern

solver.add(piece_type[4] == 1)  # Fifth Solo Traditional


def count_determined(s):
    count = 0
    for i in range(5):
        s.push()
        s.add(pianist[i] == 0)
        sat1 = s.check()
        s.pop()
        s.push()
        s.add(pianist[i] == 1)
        sat2 = s.check()
        s.pop()
        if (sat1 == sat and sat2 != sat) or (sat1 != sat and sat2 == sat):
            count += 1
    return count

result = count_determined(solver)

if result == 1:
    print("Option A is correct")
elif result == 2:
    print("Option B is correct")
elif result == 3:
    print("Option C is correct")
elif result == 4:
    print("Option D is correct")
elif result == 5:
    print("Option E is correct")