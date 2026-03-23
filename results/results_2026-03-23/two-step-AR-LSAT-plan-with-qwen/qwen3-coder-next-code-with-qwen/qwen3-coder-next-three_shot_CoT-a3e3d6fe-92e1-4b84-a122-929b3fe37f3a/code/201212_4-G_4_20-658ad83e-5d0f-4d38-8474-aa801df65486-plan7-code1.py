from z3 import *

# Article indices: G=0, H=1, J=2, Q=3, R=4, S=5, Y=6
articles = ["G", "H", "J", "Q", "R", "S", "Y"]
topic_map = {
    0: 'F', 1: 'F', 2: 'F',  # G, H, J → finance
    3: 'N', 4: 'N', 5: 'N',  # Q, R, S → nutrition
    6: 'W'                     # Y → wildlife
}

# Position variables: pos[i] = position (1-7) of article i
pos = [Int(f"pos_{i}") for i in range(7)]

# Base solver
solver = Solver()

# Domain constraints: positions 1-7
for i in range(7):
    solver.add(pos[i] >= 1, pos[i] <= 7)

# All positions distinct
solver.add(Distinct(pos))

# Consecutive articles cannot cover same topic:
# For each adjacent slot pair (k, k+1) where k=1..6,
# and for each ordered pair of articles (i,j), i≠j:
# If article i is at position k and article j at position k+1, then topics differ
for k in range(1, 7):
    for i in range(7):
        for j in range(7):
            if i != j:
                solver.add(
                    Or(
                        Not(pos[i] == k),
                        Not(pos[j] == k + 1),
                        topic_map[i] != topic_map[j]
                    )
                )

# S can be earlier than Q only if Q is third: (S < Q) → (Q == 3)
# Equivalent to: S >= Q OR Q == 3
solver.add(Or(pos[5] >= pos[3], pos[3] == 3))

# S must be earlier than Y
solver.add(pos[5] < pos[6])

# J before G, and G before R
solver.add(pos[2] < pos[0], pos[0] < pos[4])

# Answer choices: check which could be true
answer_choices = [
    ("G is second", 0, 2),   # G (index 0) at position 2
    ("H is second", 1, 2),   # H (index 1) at position 2
    ("S is second", 5, 2),   # S (index 5) at position 2
    ("R is third", 4, 3),    # R (index 4) at position 3
    ("Y is third", 6, 3)     # Y (index 6) at position 3
]

sat_choices = []
for i, (desc, art_idx, pos_val) in enumerate(answer_choices):
    s = Solver()
    # Add all base constraints
    for a in solver.assertions():
        s.add(a)
    
    # Add candidate constraint: article art_idx at position pos_val
    s.add(pos[art_idx] == pos_val)
    
    if s.check() == sat:
        sat_choices.append(desc)

print(sat_choices[0])