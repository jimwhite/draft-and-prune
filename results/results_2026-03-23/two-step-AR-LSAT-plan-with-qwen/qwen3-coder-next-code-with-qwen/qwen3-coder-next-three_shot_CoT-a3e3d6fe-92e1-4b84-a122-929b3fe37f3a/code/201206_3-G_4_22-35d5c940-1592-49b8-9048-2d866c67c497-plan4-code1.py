from z3 import *

# Solo indices: 0 to 4 (positions 1 to 5)
wayne = [Bool(f"wayne_{i}") for i in range(5)]
modern = [Bool(f"modern_{i}") for i in range(5)]

solver = Solver()

# Domain constraints: Each solo is performed by exactly one pianist, and each has a type
for i in range(5):
    solver.add(wayne[i] != Not(wayne[i]))  # tautology, but ensures Boolean nature
    solver.add(Or(wayne[i], Not(wayne[i])))  # tautology

# Fixed constraint: Solo 3 (index 2) is traditional → not modern[2]
solver.add(Not(modern[2]))

# Exactly two consecutive traditional pieces
# We need exactly one pair of consecutive trads, and no third adjacent to it
trad = [Not(modern[i]) for i in range(5)]

# Count traditional solos: must be at least 2 (for the consecutive pair) and total trads = 2 or more
# But constraint says "exactly two of the traditional pieces are performed consecutively"
# This means there is exactly one pair of consecutive trads, and no other trads adjacent to them
# So total trads = 2 (the consecutive pair) OR possibly more if isolated, but the "exactly two consecutive" means only one adjacent pair exists

# Let's define adjacency indicators for trad pairs
adj = [And(trad[i], trad[i+1]) for i in range(4)]

# Exactly one adjacent pair of trads
solver.add(Sum([If(adj[i], 1, 0) for i in range(4)]) == 1)

# No third trad adjacent to the pair: if adj[i] is true, then trad[i-1] and trad[i+2] must be false (if they exist)
# For i=0: adj[0] → not trad[2]
solver.add(Implies(adj[0], Not(trad[2])))
# For i=1: adj[1] → not trad[0] and not trad[3]
solver.add(Implies(adj[1], And(Not(trad[0]), Not(trad[3]))))
# For i=2: adj[2] → not trad[1] and not trad[4]
solver.add(Implies(adj[2], And(Not(trad[1]), Not(trad[4]))))
# For i=3: adj[3] → not trad[2]
solver.add(Implies(adj[3], Not(trad[2])))

# Fourth solo constraint (index 3): either Wayne performs traditional or Zara performs modern
# Traditional = not modern, so:
# (wayne[3] and not modern[3]) or (not wayne[3] and modern[3])
solver.add(Or(
    And(wayne[3], Not(modern[3])),
    And(Not(wayne[3]), modern[3])
))

# Different-pianist constraint: solo 2 and solo 5 different pianists
solver.add(wayne[1] != wayne[4])

# No traditional piece until Wayne performs at least one modern piece
# Let first_wayne_modern = earliest index where wayne[i] and modern[i]
# Then for any traditional solo at position i, there must be some j < i with wayne[j] and modern[j]

# We'll enforce: if trad[i] is true, then there exists j < i such that wayne[j] and modern[j]
for i in range(5):
    # If solo i is traditional, then there must be a Wayne modern before it
    solver.add(Implies(trad[i], Or([And(wayne[j], modern[j]) for j in range(i)])))

# Hypothetical: fifth solo is traditional and performed by Wayne
solver.add(wayne[4])
solver.add(Not(modern[4]))

# Answer choices (0-indexed)
answer_choices = [
    Not(wayne[0]),           # Zara performs first solo
    wayne[1],                # Wayne performs second solo
    Not(wayne[2]),           # Zara performs third solo (since third is traditional, this means Zara does it)
    modern[1],               # Second solo is modern
    Not(modern[3])           # Fourth solo is traditional
]

# Check each answer choice under the hypothetical
answer_index_list = []
for idx, constraint in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(constraint)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)