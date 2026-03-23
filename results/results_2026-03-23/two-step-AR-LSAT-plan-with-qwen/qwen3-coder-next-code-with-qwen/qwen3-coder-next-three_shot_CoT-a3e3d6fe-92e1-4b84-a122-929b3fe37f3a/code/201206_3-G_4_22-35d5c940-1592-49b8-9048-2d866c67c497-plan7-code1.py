from z3 import *

# Solo positions: 0-indexed (0=1st, 1=2nd, ..., 4=5th)
# p[i] = True if Wayne performs solo i+1, False if Zara
p = [Bool(f"p_{i}") for i in range(5)]
# t[i] = True if traditional piece, False if modern
t = [Bool(f"t_{i}") for i in range(5)]

solver = Solver()

# Fixed constraint: third solo is traditional (index 2)
solver.add(t[2] == True)

# Exactly two consecutive traditional pieces
# Count adjacent pairs that are both traditional: (0,1), (1,2), (2,3), (3,4)
adjacent_pairs = [
    And(t[0], t[1]),
    And(t[1], t[2]),
    And(t[2], t[3]),
    And(t[3], t[4])
]
# Exactly one adjacent pair is both traditional
solver.add(Sum([If(pair, 1, 0) for pair in adjacent_pairs]) == 1)

# Fourth solo constraint (index 3): Either Wayne performs traditional OR Zara performs modern
solver.add(Or(And(p[3], t[3]), And(Not(p[3]), Not(t[3]))))

# Pianist constraint: second and fifth solos (indices 1 and 4) have different pianists
solver.add(p[1] != p[4])

# No traditional piece until Wayne performs at least one modern piece
# Find first Wayne modern solo (if any)
# We'll enforce: if t[i] is True, then there must be some j < i where p[j] and Not(t[j])
# For each position i, if t[i] is True, then there exists j < i with p[j] and Not(t[j])
for i in range(5):
    if t[i] == True:  # This is always true for i=2, but we handle generally
        # Create constraint: if t[i] is True, then there exists j < i with p[j] and Not(t[j])
        # We'll use a disjunction over all possible j < i
        if i > 0:
            exists_earlier_modern_wayne = Or(*[And(p[j], Not(t[j])) for j in range(i)])
            solver.add(Implies(t[i], exists_earlier_modern_wayne))
        else:
            # i=0 cannot be traditional (no earlier Wayne modern possible)
            solver.add(Not(t[0]))

# Scenario assumption: fifth solo is Wayne and traditional (index 4)
solver.add(p[4] == True, t[4] == True)

# Answer choices (0-indexed)
answer_choices = [
    "Zara performs the first solo.",  # p[0] == False
    "Wayne performs the second solo.",  # p[1] == True
    "Zara performs the third solo.",  # p[2] == False
    "The second solo is a modern piece.",  # t[1] == False
    "The fourth solo is a traditional piece."  # t[3] == True
]

answer_index_list = []

for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    if idx == 0:  # Zara performs first solo
        s_chk.add(Not(p[0]))
    elif idx == 1:  # Wayne performs second solo
        s_chk.add(p[1] == True)
    elif idx == 2:  # Zara performs third solo
        s_chk.add(Not(p[2]))
    elif idx == 3:  # Second solo is modern
        s_chk.add(t[1] == False)
    elif idx == 4:  # Fourth solo is traditional
        s_chk.add(t[3] == True)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)