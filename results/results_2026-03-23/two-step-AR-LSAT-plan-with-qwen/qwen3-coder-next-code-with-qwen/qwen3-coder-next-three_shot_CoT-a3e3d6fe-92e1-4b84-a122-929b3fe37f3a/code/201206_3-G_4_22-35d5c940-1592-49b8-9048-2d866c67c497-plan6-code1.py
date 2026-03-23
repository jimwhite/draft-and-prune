from z3 import *

# Solo positions: 1 to 5 (0-indexed as 0 to 4 in code)
# pianist[i]: True if Wayne, False if Zara
# type[i]: True if modern, False if traditional

pianist = [Bool(f"pianist_{i}") for i in range(5)]
type_ = [Bool(f"type_{i}") for i in range(5)]

solver = Solver()

# Fixed constraint: third solo is traditional (index 2)
solver.add(type_[2] == False)

# Exactly two consecutive traditional pieces
# We need exactly one pair of consecutive trad's, and no other adjacent trad pairs

# Helper: is_trad[i] = True if solo i is traditional
is_trad = [Not(type_[i]) for i in range(5)]

# Count adjacent trad pairs
adj_trad_pairs = []
for i in range(4):
    adj_trad_pairs.append(And(is_trad[i], is_trad[i+1]))

# Exactly one adjacent trad pair
solver.add(Sum([If(pair, 1, 0) for pair in adj_trad_pairs]) == 1)

# Fourth solo constraint: Wayne trad OR Zara modern
# (pianist[3] == True and type_[3] == False) OR (pianist[3] == False and type_[3] == True)
solver.add(Or(
    And(pianist[3], Not(type_[3])),
    And(Not(pianist[3]), type_[3])
))

# Second and fifth solos by different pianists
solver.add(pianist[1] != pianist[4])

# No traditional piece until Wayne performs at least one modern piece
# For any traditional solo j, there must be a Wayne modern solo k < j

for j in range(5):
    # If solo j is traditional, then there exists k < j where Wayne plays modern
    solver.add(Implies(
        is_trad[j],
        Or([And(pianist[k], type_[k]) for k in range(j)])
    ))

# Question assumption: fifth solo is Wayne and traditional
solver.add(pianist[4] == True)
solver.add(type_[4] == False)

# Answer choices (convert to conditions):
# 0: Zara performs the first solo -> pianist[0] == False
# 1: Wayne performs the second solo -> pianist[1] == True
# 2: Zara performs the third solo -> pianist[2] == False
# 3: The second solo is a modern piece -> type_[1] == True
# 4: The fourth solo is a traditional piece -> type_[3] == False

answer_choices = [
    lambda: pianist[0] == False,
    lambda: pianist[1] == True,
    lambda: pianist[2] == False,
    lambda: type_[1] == True,
    lambda: type_[3] == False
]

answer_index_list = []

for idx, cond in enumerate(answer_choices):
    s_chk = Solver()
    # Add all base constraints
    for a in solver.assertions():
        s_chk.add(a)
    
    # Add the specific condition from the choice
    s_chk.add(cond())
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)