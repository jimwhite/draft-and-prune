from z3 import *

# Pianist indices: Wayne=0, Zara=1
# Piece types: modern=0, traditional=1

pianist = [Int(f"p_{i}") for i in range(5)]
piece = [Int(f"t_{i}") for i in range(5)]

solver = Solver()

# Domain constraints
for i in range(5):
    solver.add(pianist[i] == 0, pianist[i] == 1)
    solver.add(piece[i] == 0, piece[i] == 1)

# Fixed constraint: third solo (index 2) is traditional
solver.add(piece[2] == 1)

# Exactly two consecutive traditional pieces: exactly one adjacent pair of traditional pieces
# We need to ensure there is exactly one i such that piece[i] == 1 and piece[i+1] == 1
adjacent_pairs = []
for i in range(4):
    adjacent_pairs.append(And(piece[i] == 1, piece[i+1] == 1))

# Exactly one adjacent pair of traditional pieces
solver.add(Sum([If(pair, 1, 0) for pair in adjacent_pairs]) == 1)

# No three consecutive traditional pieces (redundant with above but explicit)
for i in range(3):
    solver.add(Not(And(piece[i] == 1, piece[i+1] == 1, piece[i+2] == 1)))

# Fourth solo constraint: (Wayne performs traditional) OR (Zara performs modern)
solver.add(Or(
    And(pianist[3] == 0, piece[3] == 1),
    And(pianist[3] == 1, piece[3] == 0)
))

# Pianist repetition constraint: pianist of solo 2 (index 1) ≠ pianist of solo 5 (index 4)
solver.add(pianist[1] != pianist[4])

# No traditional piece until Wayne performs at least one modern piece
# Find the first traditional solo and ensure there's a Wayne modern before it
first_traditional = [Int(f"ft_{i}") for i in range(5)]
# ft_i = 1 if solo i is the first traditional
for i in range(5):
    # If ft_i = 1, then piece[i] == 1 and all previous are modern
    solver.add(Implies(first_traditional[i] == 1, piece[i] == 1))
    for j in range(i):
        solver.add(Implies(first_traditional[i] == 1, piece[j] == 0))
    # If ft_i = 1 and i > 0, then there must be a Wayne modern before
    if i > 0:
        solver.add(Implies(first_traditional[i] == 1, Or(
            And(pianist[j] == 0, piece[j] == 0) for j in range(i)
        )))

# Exactly one first traditional
solver.add(Sum(first_traditional) == 1)

# Hypothesis: fifth solo is Wayne + traditional
solver.add(pianist[4] == 0, piece[4] == 1)

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
for idx, (desc, constraint_func) in enumerate(answer_choices):
    s_chk = Solver()
    # Add all base constraints + hypothesis
    for a in solver.assertions():
        s_chk.add(a)
    
    # Add the choice constraint
    s_chk.add(constraint_func())
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)