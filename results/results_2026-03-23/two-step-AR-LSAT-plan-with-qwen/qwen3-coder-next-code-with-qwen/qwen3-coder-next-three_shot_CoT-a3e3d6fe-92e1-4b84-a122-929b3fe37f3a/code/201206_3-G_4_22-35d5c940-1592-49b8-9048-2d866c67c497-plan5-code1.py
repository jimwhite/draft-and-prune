from z3 import *

# Solo positions: 1 to 5 (0-indexed as 0 to 4 in code)
# Pianists: Wayne=0, Zara=1
# modern[i] = True if solo i is modern, False if traditional

modern = [Bool(f"modern_{i}") for i in range(5)]
pianist = [Int(f"pianist_{i}") for i in range(5)]

solver = Solver()

# Domain constraints
for i in range(5):
    solver.add(Or(pianist[i] == 0, pianist[i] == 1))

# Fixed constraint: Solo 3 (index 2) is traditional
solver.add(Not(modern[2]))

# Exactly two consecutive traditional pieces
# We need exactly one pair of consecutive traditional solos
consecutive_trad = []
for i in range(4):
    # trad[i] and trad[i+1]
    consecutive_trad.append(And(Not(modern[i]), Not(modern[i+1])))

# Exactly one of these pairs is true
solver.add(Sum([If(c, 1, 0) for c in consecutive_trad]) == 1)

# Fourth solo constraint (index 3): 
# (Wayne performs traditional) OR (Zara performs modern)
solver.add(Or(
    And(pianist[3] == 0, Not(modern[3])),
    And(pianist[3] == 1, modern[3])
))

# Non-repetition constraint: pianist of solo 2 != pianist of solo 5
solver.add(pianist[1] != pianist[4])

# No traditional piece until Wayne performs at least one modern piece
# For each solo i, if it's traditional (Not(modern[i])), then there must be some earlier solo k < i
# where Wayne performs a modern piece (pianist[k]==0 and modern[k]==True)
for i in range(5):
    # If solo i is traditional, then there exists k < i such that pianist[k]==0 and modern[k]==True
    wayne_modern_before = Or(*[
        And(pianist[k] == 0, modern[k]) for k in range(i)
    ])
    solver.add(Implies(Not(modern[i]), wayne_modern_before))

# Problem assumption: Solo 5 (index 4) is Wayne and traditional
solver.add(pianist[4] == 0)
solver.add(Not(modern[4]))

# Answer choices
answer_choices = [
    ("Zara performs the first solo.", pianist[0] == 1),
    ("Wayne performs the second solo.", pianist[1] == 0),
    ("Zara performs the third solo.", pianist[2] == 1),
    ("The second solo is a modern piece.", modern[2]),  # Note: "modem" typo in question, should be "modern"
    ("The fourth solo is a traditional piece.", Not(modern[3]))
]

# Check each answer choice
answer_index_list = []
for idx, (desc, assertion) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(assertion)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)