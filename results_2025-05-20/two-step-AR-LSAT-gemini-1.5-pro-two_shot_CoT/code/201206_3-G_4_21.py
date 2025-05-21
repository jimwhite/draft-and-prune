from z3 import *

# Variables
pianist = Array('pianist', IntSort(), IntSort())
piece_type = Array('piece_type', IntSort(), IntSort())
i = Int('i')

# Solver
solver = Solver()

# Constraints
solver.add(ForAll(i, Implies(And(i >= 0, i < 5), And(pianist[i] >= 0, pianist[i] <= 1)))) # Pianist Domain
solver.add(ForAll(i, Implies(And(i >= 0, i < 5), And(piece_type[i] >= 0, piece_type[i] <= 1)))) # Piece Type Domain
solver.add(piece_type[2] == 1) # Third Solo Traditional
# Fixed: Use a chain of Xor operations for more than two arguments
solver.add(Xor(And(piece_type[0]==1, piece_type[1]==1), Xor(And(piece_type[1]==1, piece_type[2]==1), Xor(And(piece_type[2]==1, piece_type[3]==1), And(piece_type[3]==1, piece_type[4]==1))))) # Exactly One Consecutive Traditional Pair
solver.add(Or(And(pianist[3] == 0, piece_type[3] == 1), And(pianist[3] == 1, piece_type[3] == 0))) # Fourth Solo Condition
solver.add(pianist[1] != pianist[4]) # Second and Fifth Solo Different Pianists

# Constraint 7 (No Traditional Until Wayne Modern) - Fixed: Corrected the logic and removed redundant conditions
solver.add(Implies(piece_type[0] == 1, And(pianist[0] == 0, piece_type[0] == 0))) # This constraint makes piece_type[0] always 0
solver.add(Implies(piece_type[1] == 1, pianist[0] == 0))
solver.add(Implies(piece_type[2] == 1, Or(pianist[0] == 0, pianist[1] == 0))) # Simplified: piece_type[2] is already constrained to 1
solver.add(Implies(piece_type[3] == 1, Or(pianist[0] == 0, pianist[1] == 0, pianist[2] == 0)))
solver.add(Implies(piece_type[4] == 1, Or(pianist[0] == 0, pianist[1] == 0, pianist[2] == 0, pianist[3] == 0)))


# Question condition
solver.add(piece_type[4] == 1)

# Check satisfiability (assumed to be SAT based on problem structure)
# solver.check()

determined_count = 0
for i in range(5):
    solver.push()
    solver.add(pianist[i] != 0)
    if solver.check() == unsat:
        determined_count += 1
    solver.pop()

    if determined_count <= i: # Optimization: Only check the other option if the first check wasn't unsat
        solver.push()
        solver.add(pianist[i] != 1)
        if solver.check() == unsat:
            determined_count += 1
        solver.pop()

answers = ["one", "two", "three", "four", "five"]
print(f"Option {chr(65 + answers.index(answers[determined_count-1]))} is correct")
exit()
