from z3 import *

# Solo positions: 1 to 5 (0-indexed as 0 to 4 in code)
# Pianist: 0 for Wayne, 1 for Zara
pianist = [Int(f"p_{i}") for i in range(5)]
# Modern: True (1) if modern, False (0) if traditional
modern = [Bool(f"M_{i}") for i in range(5)]

solver = Solver()

# Domain constraints
for i in range(5):
    solver.add(pianist[i] == 0, pianist[i] == 1)  # Wayne or Zara

# Fixed constraints
# Solo 3 is traditional (index 2)
solver.add(Not(modern[2]))

# Exactly two traditional pieces are performed consecutively
# Count consecutive pairs (i, i+1) where both are traditional (not modern)
consecutive_trad = []
for i in range(4):
    consecutive_trad.append(And(Not(modern[i]), Not(modern[i+1])))

# Exactly one such consecutive pair exists
solver.add(Sum([If(c, 1, 0) for c in consecutive_trad]) == 1)

# In solo 4 (index 3): (Wayne and traditional) or (Zara and modern)
solver.add(Or(
    And(pianist[3] == 0, Not(modern[3])),
    And(pianist[3] == 1, modern[3])
))

# Pianist of solo 2 != pianist of solo 5 (indices 1 and 4)
solver.add(pianist[1] != pianist[4])

# No traditional piece before Wayne performs at least one modern piece
# Find first Wayne modern solo, then ensure no traditional before it
wayne_modern_positions = [And(pianist[i] == 0, modern[i]) for i in range(5)]

# Wayne must perform at least one modern piece
solver.add(Or(*wayne_modern_positions))

# For each position i, if there's a traditional piece at i, then Wayne must have performed
# a modern piece at some position j <= i
for i in range(5):
    # If solo i is traditional, then there must be a Wayne modern piece at or before i
    solver.add(Implies(
        Not(modern[i]),
        Or([And(pianist[j] == 0, modern[j]) for j in range(i+1)])
    ))

# Hypothesis: fifth solo is Wayne performing traditional piece (index 4)
solver.add(pianist[4] == 0, Not(modern[4]))

# Answer choices (indices: A=0, B=1, C=2, D=3, E=4)
answer_choices = [
    pianist[0] == 1,  # Zara performs first solo
    pianist[1] == 0,  # Wayne performs second solo
    pianist[2] == 1,  # Zara performs third solo
    modern[1],        # Second solo is modern
    Not(modern[3])    # Fourth solo is traditional
]

# Check each answer choice
answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(choice)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)