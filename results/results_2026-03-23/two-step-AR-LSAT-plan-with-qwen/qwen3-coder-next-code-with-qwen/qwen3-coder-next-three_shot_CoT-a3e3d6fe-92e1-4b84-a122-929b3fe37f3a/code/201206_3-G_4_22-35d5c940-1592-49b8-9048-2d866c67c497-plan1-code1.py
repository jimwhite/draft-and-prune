from z3 import *

# Pianist indices: Wayne=0, Zara=1
# Piece type indices: modern=0, traditional=1

pianist = [Int(f"p_{i}") for i in range(5)]
piece = [Int(f"t_{i}") for i in range(5)]

solver = Solver()

# Domain constraints
for i in range(5):
    solver.add(pianist[i] == 0, pianist[i] == 1)  # Only Wayne or Zara
    solver.add(piece[i] == 0, piece[i] == 1)     # Only modern or traditional

# Fixed constraint: third solo (index 2) is traditional
solver.add(piece[2] == 1)

# Exactly two consecutive traditional pieces constraint:
# We need exactly one pair of adjacent solos both being traditional
adjacent_pairs = [(i, i+1) for i in range(4)]
# For each pair, create a boolean indicating if both are traditional
is_consecutive_trad = [And(piece[i] == 1, piece[i+1] == 1) for i in range(4)]
# Exactly one of these pairs is true
solver.add(Sum([If(pair, 1, 0) for pair in is_consecutive_trad]) == 1)

# Fourth solo (index 3) constraint: 
# Either Wayne performs traditional OR Zara performs modern
solver.add(Or(
    And(pianist[3] == 0, piece[3] == 1),
    And(pianist[3] == 1, piece[3] == 0)
))

# Second and fifth solo constraint: different pianists
solver.add(pianist[1] != pianist[4])

# No traditional piece before Wayne performs at least one modern piece
# For each position i, if piece[i] == 1 (traditional), then there must be some j < i
# where pianist[j] == 0 (Wayne) and piece[j] == 0 (modern)
for i in range(5):
    # If this is a traditional piece, there must be an earlier Wayne modern solo
    solver.add(Implies(
        piece[i] == 1,
        Or([And(pianist[j] == 0, piece[j] == 0) for j in range(i)])
    ))

# Scenario assumption: fifth solo is Wayne performing traditional
solver.add(pianist[4] == 0)
solver.add(piece[4] == 1)

# Answer choices
answer_choices = [
    ("Zara performs the first solo.", lambda: pianist[0] == 1),
    ("Wayne performs the second solo.", lambda: pianist[1] == 0),
    ("Zara performs the third solo.", lambda: pianist[2] == 1),
    ("The second solo is a modern piece.", lambda: piece[1] == 0),
    ("The fourth solo is a traditional piece.", lambda: piece[3] == 1)
]

# Check each answer choice
answer_index_list = []
for idx, (desc, condition) in enumerate(answer_choices):
    s_chk = Solver()
    # Add all base constraints and scenario
    for a in solver.assertions():
        s_chk.add(a)
    
    # Add the condition for this choice
    s_chk.add(condition())
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)