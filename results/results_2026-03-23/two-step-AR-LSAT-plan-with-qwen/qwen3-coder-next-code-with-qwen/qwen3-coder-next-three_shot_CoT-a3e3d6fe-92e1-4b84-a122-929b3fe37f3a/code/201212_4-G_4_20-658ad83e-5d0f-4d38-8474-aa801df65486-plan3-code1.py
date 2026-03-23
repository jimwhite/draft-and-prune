from z3 import *

# Article indices: G=0, H=1, J=2, Q=3, R=4, S=5, Y=6
articles = ["G", "H", "J", "Q", "R", "S", "Y"]
pos = [Int(f"pos_{i}") for i in range(7)]

# Base solver
solver = Solver()

# Domain constraints: positions 1-7, all distinct
for i in range(7):
    solver.add(pos[i] >= 1, pos[i] <= 7)
solver.add(Distinct(*pos))

# Topic grouping: finance={G,H,J}, nutrition={Q,R,S}, wildlife={Y}
def topic(i):
    if i in [0, 1, 2]:  # G, H, J
        return 0  # finance
    elif i in [3, 4, 5]:  # Q, R, S
        return 1  # nutrition
    else:  # Y (index 6)
        return 2  # wildlife

# Consecutive articles cannot cover the same topic
for k in range(1, 7):  # positions 1 through 6 (0-indexed positions in the sequence)
    for i in range(7):
        for j in range(7):
            if i != j and topic(i) == topic(j):
                # If article i is at position k and article j is at position k+1, this is invalid
                solver.add(Or(pos[i] != k, pos[j] != k+1))

# Conditional constraint: S can be earlier than Q only if Q is third
# Equivalent to: (pos_S >= pos_Q) OR (pos_Q == 3)
solver.add(Or(pos[5] >= pos[3], pos[3] == 3))

# S must be earlier than Y
solver.add(pos[5] < pos[6])

# J must be earlier than G, and G must be earlier than R
solver.add(pos[0] < pos[2])  # J before G? Wait, J is index 2, G is index 0
# Correction: J must be earlier than G → pos_J < pos_G → pos[2] < pos[0]
# G must be earlier than R → pos_G < pos_R → pos[0] < pos[4]
solver.add(pos[2] < pos[0])
solver.add(pos[0] < pos[4])

# Answer choices: check which could be true
answer_choices = [
    ("G is second", 0, 2),   # G (index 0) at position 2
    ("H is second", 1, 2),   # H (index 1) at position 2
    ("S is second", 5, 2),   # S (index 5) at position 2
    ("R is third", 4, 3),    # R (index 4) at position 3
    ("Y is third", 6, 3)     # Y (index 6) at position 3
]

answer_index_list = []
for idx, (_, article_idx, position) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraint that this article is at the specified position
    s_chk.add(pos[article_idx] == position)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)