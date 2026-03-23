from z3 import *

# Article indices: G=0, H=1, J=2 (finance); Q=3, R=4, S=5 (nutrition); Y=6 (wildlife)
articles = ["G", "H", "J", "Q", "R", "S", "Y"]
finance = [0, 1, 2]
nutrition = [3, 4, 5]
wildlife = [6]

# Position variables: pos[i] is the editing position of article i (1 to 7)
pos = [Int(f"pos_{i}") for i in range(7)]

# Base solver
solver = Solver()

# Domain constraints: each position between 1 and 7, all distinct
for i in range(7):
    solver.add(pos[i] >= 1, pos[i] <= 7)
solver.add(Distinct(*pos))

# No consecutive same-topic constraint
# For any two articles i and j with the same topic, they cannot be adjacent (|pos[i] - pos[j]| != 1)
def same_topic(i, j):
    if i in finance and j in finance:
        return True
    if i in nutrition and j in nutrition:
        return True
    if i in wildlife and j in wildlife:
        return True
    return False

for i in range(7):
    for j in range(i+1, 7):
        if same_topic(i, j):
            solver.add(Abs(pos[i] - pos[j]) != 1)

# S before Y constraint: S (index 5) must be earlier than Y (index 6)
solver.add(pos[5] < pos[6])

# J before G before R constraint: J (2) < G (0) < R (4)
solver.add(pos[2] < pos[0])
solver.add(pos[0] < pos[4])

# S before Q conditional: If S is earlier than Q, then Q must be third
# (pos[5] < pos[3]) => (pos[3] == 3)
# Equivalent to: (pos[5] >= pos[3]) OR (pos[3] == 3)
solver.add(Or(pos[5] >= pos[3], pos[3] == 3))

# Answer choices: check which could be true
answer_choices = [
    ("G is second", 0, 2),   # G (index 0) at position 2
    ("H is second", 1, 2),   # H (index 1) at position 2
    ("S is second", 5, 2),   # S (index 5) at position 2
    ("R is third", 4, 3),    # R (index 4) at position 3
    ("Y is third", 6, 3)     # Y (index 6) at position 3
]

answer_index_list = []
for idx, (_, article_idx, target_pos) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraint for the specific choice
    s_chk.add(pos[article_idx] == target_pos)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)