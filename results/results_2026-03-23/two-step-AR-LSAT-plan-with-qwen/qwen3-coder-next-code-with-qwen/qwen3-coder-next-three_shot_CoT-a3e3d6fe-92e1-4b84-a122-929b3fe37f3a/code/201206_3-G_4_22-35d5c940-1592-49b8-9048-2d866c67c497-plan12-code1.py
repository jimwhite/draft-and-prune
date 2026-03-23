from z3 import *

# Pianist indices: Wayne=0, Zara=1
# Piece type indices: modern=0, traditional=1

# Variables for each solo (0-indexed positions 0-4)
pianist = [Int(f"p_{i}") for i in range(5)]
piece = [Int(f"t_{i}") for i in range(5)]

solver = Solver()

# Domain constraints: pianist ∈ {0,1}, piece ∈ {0,1}
for i in range(5):
    solver.add(Or(pianist[i] == 0, pianist[i] == 1))
    solver.add(Or(piece[i] == 0, piece[i] == 1))

# Fixed constraint: Solo 3 (index 2) is traditional
solver.add(piece[2] == 1)

# Exactly two consecutive traditional pieces (form a single block of length 2)
# We need exactly one pair of adjacent trad. pieces, and no third trad piece adjacent to them
# Possible positions for the block: (0,1), (1,2), (2,3), (3,4)
# But position 2 is fixed as trad., so block must include index 2: either (1,2) or (2,3)

# Let's define binary variables for each possible block position
block_01 = Bool("block_01")  # trad at 0 and 1
block_12 = Bool("block_12")  # trad at 1 and 2
block_23 = Bool("block_23")  # trad at 2 and 3
block_34 = Bool("block_34")  # trad at 3 and 4

# Exactly one block is active
solver.add(AtMost(block_01, block_12, block_23, block_34, 1))
solver.add(Or(block_01, block_12, block_23, block_34))

# Link blocks to actual piece types
solver.add(Implies(block_01, And(piece[0] == 1, piece[1] == 1)))
solver.add(Implies(block_12, And(piece[1] == 1, piece[2] == 1)))
solver.add(Implies(block_23, And(piece[2] == 1, piece[3] == 1)))
solver.add(Implies(block_34, And(piece[3] == 1, piece[4] == 1)))

# Ensure no extra trad pieces adjacent to the block
# If block_01 is active, then piece[2] must be modern (but it's fixed to 1) → impossible
# So block_01 is impossible due to piece[2]=1
solver.add(Not(block_01))

# If block_34 is active, then piece[2] must be modern (but it's fixed to 1) → impossible
solver.add(Not(block_34))

# So only block_12 or block_23 possible
solver.add(Or(block_12, block_23))

# Additional constraints to ensure exactly two consecutive trad pieces:
# If block_12 is active, then piece[3] must be modern (to avoid 3 consecutive)
solver.add(Implies(block_12, piece[3] == 0))
# If block_23 is active, then piece[1] must be modern (to avoid 3 consecutive)
solver.add(Implies(block_23, piece[1] == 0))

# Solo 4 constraint: Either (Wayne performs and trad.) or (Zara performs and modern)
# Index 3 is solo 4
solver.add(Or(
    And(pianist[3] == 0, piece[3] == 1),
    And(pianist[3] == 1, piece[3] == 0)
))

# Pianist for solo 2 ≠ pianist for solo 5 (indices 1 and 4)
solver.add(pianist[1] != pianist[4])

# No trad. piece until Wayne performs at least one modern piece
# Let first_wayne_modern be the first position where pianist==0 and piece==0
# We'll enforce: if a solo is traditional, then there must be some earlier solo where Wayne performed modern

# For each position i, if piece[i] == 1 (traditional), then there exists j < i such that
# pianist[j] == 0 and piece[j] == 0

for i in range(5):
    # Create helper variables for existence of earlier Wayne-modern
    earlier_wayne_modern = Bool(f"ewm_{i}")
    
    # Build disjunction of Wayne-modern at positions < i
    if i == 0:
        solver.add(Not(earlier_wayne_modern))
    else:
        disjuncts = []
        for j in range(i):
            disjuncts.append(And(pianist[j] == 0, piece[j] == 0))
        solver.add(earlier_wayne_modern == Or(*disjuncts))
    
    # If piece[i] is traditional, then earlier Wayne-modern must exist
    solver.add(Implies(piece[i] == 1, earlier_wayne_modern))

# Conditional scenario: fifth solo (index 4) is Wayne performing traditional
solver.add(pianist[4] == 0)
solver.add(piece[4] == 1)

# Answer options
options = [
    ("Zara performs the first solo.", lambda: pianist[0] == 1),
    ("Wayne performs the second solo.", lambda: pianist[1] == 0),
    ("Zara performs the third solo.", lambda: pianist[2] == 1),
    ("The second solo is a modem piece.", lambda: piece[1] == 0),
    ("The fourth solo is a traditional piece.", lambda: piece[3] == 1)
]

answer_index_list = []
for idx, (desc, constraint_func) in enumerate(options):
    s_chk = Solver()
    # Add all base constraints
    for a in solver.assertions():
        s_chk.add(a)
    
    # Add conditional scenario (already added above, but ensure it's there)
    s_chk.add(pianist[4] == 0)
    s_chk.add(piece[4] == 1)
    
    # Add option constraint
    s_chk.add(constraint_func())
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)