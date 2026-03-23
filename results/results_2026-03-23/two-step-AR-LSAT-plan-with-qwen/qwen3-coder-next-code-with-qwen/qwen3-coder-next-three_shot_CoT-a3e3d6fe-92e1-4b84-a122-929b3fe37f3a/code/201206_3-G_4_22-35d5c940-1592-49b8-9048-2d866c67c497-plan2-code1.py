from z3 import *

# Solo positions: 0 to 4 (1-indexed: 1 to 5)
pianist = [Bool(f"pianist_{i}") for i in range(5)]  # True = Wayne, False = Zara
type_ = [Bool(f"type_{i}") for i in range(5)]       # True = traditional, False = modern

solver = Solver()

# Fixed constraints
# Solo 3 is traditional (index 2)
solver.add(type_[2] == True)

# Exactly two traditional pieces are performed consecutively
# This means there is exactly one pair of adjacent solos where both are traditional,
# and no other adjacent traditional pairs (i.e., total count of adjacent true pairs = 1)
adjacent_pairs = []
for i in range(4):
    adjacent_pairs.append(And(type_[i], type_[i+1]))
solver.add(Sum([If(pair, 1, 0) for pair in adjacent_pairs]) == 1)

# In solo 4: Wayne performs traditional OR Zara performs modern
# (index 3)
solver.add(Or(And(pianist[3] == True, type_[3] == True),
              And(pianist[3] == False, type_[3] == False)))

# Pianist of solo 2 ≠ pianist of solo 5 (indices 1 and 4)
solver.add(pianist[1] != pianist[4])

# No traditional piece is performed until Wayne performs at least one modern piece
# Let first_Wayne_modern be the earliest solo where Wayne plays a modern piece.
# For all solos before that, type must be modern (False).
# We model this by: if a solo is traditional, then there must have been a Wayne modern before it.
# Equivalent: For each solo i, if type_[i] is True, then there exists j < i such that
# pianist[j] == True and type_[j] == False.
for i in range(5):
    solver.add(Implies(type_[i],
                       Or([And(pianist[j] == True, type_[j] == False) for j in range(i)])))

# Scenario assumption: fifth solo is Wayne performing a traditional piece (index 4)
solver.add(pianist[4] == True, type_[4] == True)

# Answer choices
answer_choices = [
    ("Zara performs the first solo.", lambda: pianist[0] == False),
    ("Wayne performs the second solo.", lambda: pianist[1] == True),
    ("Zara performs the third solo.", lambda: pianist[2] == False),
    ("The second solo is a modern piece.", lambda: type_[1] == False),
    ("The fourth solo is a traditional piece.", lambda: type_[3] == True)
]

# Check each choice
possible_choices_indices = []
for idx, (desc, constraint) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(constraint())
    
    if s_chk.check() == sat:
        possible_choices_indices.append(idx)

print(possible_choices_indices)