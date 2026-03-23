from z3 import *

# Create variables for 5 solos (0-indexed: positions 0 to 4)
pianist = [Int(f"pianist_{i}") for i in range(5)]  # 0=Wayne, 1=Zara
type_ = [Int(f"type_{i}") for i in range(5)]       # 0=modern, 1=traditional

solver = Solver()

# Domain constraints
for i in range(5):
    solver.add(pianist[i] == 0, pianist[i] == 1)  # Actually need Or constraint
    solver.add(type_[i] == 0, type_[i] == 1)

# Fix domain constraints properly
for i in range(5):
    solver.add(Or(pianist[i] == 0, pianist[i] == 1))
    solver.add(Or(type_[i] == 0, type_[i] == 1))

# Fixed constraints from conditions
# Third solo is traditional: position 2 (0-indexed)
solver.add(type_[2] == 1)

# Exactly two traditional pieces are consecutive
# We need exactly one pair of adjacent solos both being traditional, and no other adjacent traditional pairs
# Create boolean variables for each adjacent pair being both traditional
adjacent_pairs = []
for i in range(4):
    adj = Bool(f"adj_{i}")
    solver.add(adj == And(type_[i] == 1, type_[i+1] == 1))
    adjacent_pairs.append(adj)

# Exactly one of these pairs is true
solver.add(Sum([If(adj, 1, 0) for adj in adjacent_pairs]) == 1)

# In fourth solo (index 3), either Wayne performs traditional or Zara performs modern
solver.add(Or(
    And(pianist[3] == 0, type_[3] == 1),
    And(pianist[3] == 1, type_[3] == 0)
))

# Pianist of second solo ≠ pianist of fifth solo (indices 1 and 4)
solver.add(pianist[1] != pianist[4])

# No traditional piece until Wayne performs at least one modern piece
# Find first position where Wayne performs a modern piece, then all solos before the first traditional must be before that
# Equivalent: there exists some position k where pianist[k]==0 and type_[k]==0, and for all positions i < k, type_[i] == 0
# We can express this by: the first traditional solo occurs after some Wayne modern solo

# Create a variable for the position of first Wayne modern piece
wayne_modern_positions = [Bool(f"wm_{i}") for i in range(5)]
for i in range(5):
    solver.add(wayne_modern_positions[i] == And(pianist[i] == 0, type_[i] == 0))

# At least one Wayne modern piece exists
solver.add(Or(*wayne_modern_positions))

# For each position i, if there's a Wayne modern piece at position j <= i, then type_[i] could be traditional
# But we need: if type_[i] == 1 (traditional), then there must be some j < i where Wayne modern piece occurs
# Actually: the first traditional solo must occur after at least one Wayne modern piece
# So for all i, if type_[i] == 1, then there exists j < i such that Wayne modern piece at j

# Simpler: find the first traditional position, and ensure there's a Wayne modern before it
first_trad = Int("first_trad")
solver.add(And(first_trad >= 0, first_trad <= 4))
for i in range(5):
    solver.add(Implies(type_[i] == 1, first_trad <= i))
for i in range(5):
    solver.add(Implies(i == first_trad, type_[i] == 1))

# Ensure there's a Wayne modern piece before first_trad
wayne_modern_before_first = Bool("wayne_modern_before_first")
solver.add(wayne_modern_before_first == Or(*[And(wayne_modern_positions[j], j < first_trad) for j in range(5)]))
solver.add(wayne_modern_before_first)

# Problem-specific assumption: fifth solo is Wayne performing traditional
solver.add(pianist[4] == 0)
solver.add(type_[4] == 1)

# Answer choices
answer_choices = [
    ("Zara performs the first solo.", lambda: pianist[0] == 1),
    ("Wayne performs the second solo.", lambda: pianist[1] == 0),
    ("Zara performs the third solo.", lambda: pianist[2] == 1),
    ("The second solo is a modem piece.", lambda: type_[1] == 0),
    ("The fourth solo is a traditional piece.", lambda: type_[3] == 1)
]

answer_index_list = []
for idx, (_, constraint_func) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraint for this choice
    s_chk.add(constraint_func())
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)