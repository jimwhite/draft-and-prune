from z3 import *

# Variables
pianist = Array('pianist', IntSort(), IntSort())
piece_type = Array('piece_type', IntSort(), IntSort())

solver = Solver()

# Constraint 1 & 2 (Domains)
for i in range(5):
    solver.add(Or(pianist[i] == 0, pianist[i] == 1))
    solver.add(Or(piece_type[i] == 0, piece_type[i] == 1))

# Constraint 3 (Third Solo Traditional)
solver.add(piece_type[2] == 1)

# Constraint 4 (Exactly Two Consecutive Traditional)
consecutive_pairs = [And(piece_type[i] == 1, piece_type[i+1] == 1) for i in range(4)]
solver.add(PbEq([(pair, 1) for pair in consecutive_pairs], 1)) # Use PbEq for Exactly constraint

# Constraint 5 (Fourth Solo)
solver.add(Or(And(pianist[3] == 0, piece_type[3] == 1), And(pianist[3] == 1, piece_type[3] == 0)))

# Constraint 6 (Second and Fifth Solo Pianists Different)
solver.add(pianist[1] != pianist[4])

# Constraint 7 (No Traditional Until Wayne Modern)
j = Int('j') # Define j outside the loop
for i in range(5):
    solver.add(Implies(piece_type[i] == 1, Exists([j], And(j >= 0, j < 5, pianist[j] == 0, piece_type[j] == 0, j < i))))


# Answer Choices
options = [
    [0, 2, 3],  # A
    [1, 2, 3],  # B
    [2, 3],  # C
    [2, 4],  # D
    [3, 4]   # E
]

for option_index, option in enumerate(options):
    solver.push()
    for i in range(5):
        solver.add(piece_type[i] == (1 if i in option else 0))
    if solver.check() == sat:
        print(f"Option {chr(65 + option_index)} is correct")
        exit()
    solver.pop()

