from z3 import *

# Solo indices: 0-4 (positions 1-5)
pianist = [Int(f"pianist_{i}") for i in range(5)]
piece = [Int(f"piece_{i}") for i in range(5)]

solver = Solver()

# Domain constraints
for i in range(5):
    solver.add(pianist[i] == 0, pianist[i] == 1)  # Wayne=0, Zara=1
    solver.add(piece[i] == 0, piece[i] == 1)     # modern=0, traditional=1

# Fixed constraint: Solo 3 (index 2) is traditional
solver.add(piece[2] == 1)

# Exactly two consecutive traditional pieces constraint
# Define pair indicators for each adjacent position
pair0 = And(piece[0] == 1, piece[1] == 1)
pair1 = And(piece[1] == 1, piece[2] == 1)
pair2 = And(piece[2] == 1, piece[3] == 1)
pair3 = And(piece[3] == 1, piece[4] == 1)

# Exactly one adjacent pair of traditional pieces
solver.add(Or(pair0, pair1, pair2, pair3))
solver.add(Not(And(pair0, pair1)))
solver.add(Not(And(pair0, pair2)))
solver.add(Not(And(pair0, pair3)))
solver.add(Not(And(pair1, pair2)))
solver.add(Not(And(pair1, pair3)))
solver.add(Not(And(pair2, pair3)))

# Ensure the pair is isolated (no adjacent third traditional piece)
solver.add(Implies(pair0, And(piece[2] == 0)))
solver.add(Implies(pair1, And(piece[0] == 0, piece[3] == 0)))
solver.add(Implies(pair2, And(piece[1] == 0, piece[4] == 0)))
solver.add(Implies(pair3, And(piece[2] == 0)))

# Fourth solo constraint: (Wayne performs traditional) OR (Zara performs modern)
solver.add(Or(And(pianist[3] == 0, piece[3] == 1), And(pianist[3] == 1, piece[3] == 0)))

# Second and fifth pianist constraint: different pianists
solver.add(pianist[1] != pianist[4])

# No traditional piece until Wayne performs at least one modern piece
# Since solo 3 (index 2) is traditional, there must be Wayne+modern before index 2
# For each position j where piece[j] == 1, there must be some i < j with pianist[i]==0 and piece[i]==0
# For j=0: piece[0] cannot be 1 (since no prior position exists)
solver.add(piece[0] == 0)

# For j=1: if piece[1]==1, then there must be Wayne+modern at position 0
solver.add(Implies(piece[1] == 1, And(pianist[0] == 0, piece[0] == 0)))

# For j=2: if piece[2]==1 (which it is), then there must be Wayne+modern at position 0 or 1
solver.add(Implies(piece[2] == 1, Or(
    And(pianist[0] == 0, piece[0] == 0),
    And(pianist[1] == 0, piece[1] == 0)
)))

# For j=3: if piece[3]==1, then there must be Wayne+modern at position 0,1, or 2
solver.add(Implies(piece[3] == 1, Or(
    And(pianist[0] == 0, piece[0] == 0),
    And(pianist[1] == 0, piece[1] == 0),
    And(pianist[2] == 0, piece[2] == 0)
)))

# For j=4: if piece[4]==1, then there must be Wayne+modern at position 0-3
solver.add(Implies(piece[4] == 1, Or(
    And(pianist[0] == 0, piece[0] == 0),
    And(pianist[1] == 0, piece[1] == 0),
    And(pianist[2] == 0, piece[2] == 0),
    And(pianist[3] == 0, piece[3] == 0)
)))

# Hypothetical condition: fifth solo (index 4) is Wayne + traditional
solver.add(pianist[4] == 0, piece[4] == 1)

# Answer choices
answer_choices = [
    ("Zara performs the first solo.", lambda: pianist[0] == 1),
    ("Wayne performs the second solo.", lambda: pianist[1] == 0),
    ("Zara performs the third solo.", lambda: pianist[2] == 1),
    ("The second solo is a modern piece.", lambda: piece[1] == 0),
    ("The fourth solo is a traditional piece.", lambda: piece[3] == 1)
]

answer_index_list = []
for idx, (desc, constraint) in enumerate(answer_choices):
    s_chk = Solver()
    # Add all base constraints
    for a in solver.assertions():
        s_chk.add(a)
    # Add the hypothetical condition (already added to base solver, but ensure it's there)
    s_chk.add(pianist[4] == 0, piece[4] == 1)
    # Add the specific choice constraint
    s_chk.add(constraint())
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)