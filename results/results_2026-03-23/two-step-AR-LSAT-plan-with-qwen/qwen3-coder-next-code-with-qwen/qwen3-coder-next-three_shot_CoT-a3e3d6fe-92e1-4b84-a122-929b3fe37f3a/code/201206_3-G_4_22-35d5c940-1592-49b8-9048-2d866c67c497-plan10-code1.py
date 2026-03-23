from z3 import *

# Solo positions: 0 to 4 (1st to 5th)
p = [Int(f"p_{i}") for i in range(5)]  # pianist: 0=Wayne, 1=Zara
m = [Bool(f"m_{i}") for i in range(5)]  # m[i] = True if modern, False if traditional

solver = Solver()

# Domain constraints
for i in range(5):
    solver.add(p[i] == 0, p[i] == 1)  # Actually: p[i] must be either 0 or 1
    solver.add(Or(m[i], Not(m[i])))   # m[i] is boolean (redundant but safe)

# Fixed constraint: third solo is traditional
solver.add(Not(m[2]))

# Exactly two consecutive traditional pieces (exactly one adjacent pair)
# We'll use a counting approach: count how many adjacent pairs are both traditional
adjacent_pairs = [
    And(m[0], m[1]),
    And(m[1], m[2]),
    And(m[2], m[3]),
    And(m[3], m[4])
]
# Exactly one of these pairs is true
solver.add(Sum([If(pair, 1, 0) for pair in adjacent_pairs]) == 1)

# Fourth solo constraint: (Wayne performs traditional) OR (Zara performs modern)
solver.add(Or(
    And(p[3] == 0, Not(m[3])),
    And(p[3] == 1, m[3])
))

# Second and fifth constraint: different pianists
solver.add(p[1] != p[4])

# No traditional piece until Wayne performs at least one modern piece
# We'll implement: if a solo is traditional, then there must be an earlier solo where Wayne performed a modern piece
for i in range(5):
    # If m[i] is False (traditional), then there exists k < i such that p[k]=0 and m[k]=True
    if i > 0:
        # For each position i, enforce: m[i] = False => OR_{k=0}^{i-1} (p[k]=0 AND m[k]=True)
        solver.add(Implies(
            Not(m[i]),
            Or([And(p[k] == 0, m[k]) for k in range(i)])
        ))

# Hypothesis: fifth solo is Wayne + traditional
solver.add(p[4] == 0)
solver.add(Not(m[4]))

# Answer choices
answer_choices = [
    ("Zara performs the first solo.", lambda: p[0] == 1),
    ("Wayne performs the second solo.", lambda: p[1] == 0),
    ("Zara performs the third solo.", lambda: p[2] == 1),
    ("The second solo is a modern piece.", lambda: m[1]),
    ("The fourth solo is a traditional piece.", lambda: Not(m[3]))
]

# Check each answer choice
answer_index_list = []
for idx, (desc, constraint) in enumerate(answer_choices):
    s_chk = Solver()
    # Add all base constraints + hypothesis
    for a in solver.assertions():
        s_chk.add(a)
    
    # Add the specific choice constraint
    s_chk.add(constraint())
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)