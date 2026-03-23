from z3 import *

# Article indices: G=0, H=1, J=2, Q=3, R=4, S=5, Y=6
articles = ["G", "H", "J", "Q", "R", "S", "Y"]
# Topic mapping: 0=finance, 1=nutrition, 2=wildlife
topic = [0, 0, 0, 1, 1, 1, 2]  # G,H,J=finance; Q,R,S=nutrition; Y=wildlife

# Position variables: pos[i] = position (1-7) of article i
pos = [Int(f"pos_{i}") for i in range(7)]

# Base solver
solver = Solver()

# Domain constraints: positions 1-7 and all distinct
for i in range(7):
    solver.add(pos[i] >= 1, pos[i] <= 7)
solver.add(Distinct(*pos))

# Consecutive articles cannot cover the same topic
for i in range(7):
    for j in range(i + 1, 7):
        # If articles i and j are consecutive (|pos[i] - pos[j]| == 1), they must have different topics
        solver.add(Implies(Abs(pos[i] - pos[j]) == 1, topic[i] != topic[j]))

# S can be earlier than Q only if Q is third: (pos_S < pos_Q) → (pos_Q == 3)
# Equivalent to: (pos_S >= pos_Q) ∨ (pos_Q == 3)
solver.add(Or(pos[5] >= pos[3], pos[3] == 3))

# S must be earlier than Y: pos_S < pos_Y
solver.add(pos[5] < pos[6])

# J must be earlier than G, and G must be earlier than R: pos_J < pos_G < pos_R
solver.add(pos[2] < pos[0], pos[0] < pos[4])

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
    
    # Add constraint: article at target position
    s_chk.add(pos[article_idx] == target_pos)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

# Output the first valid choice (as per question format)
if answer_index_list:
    print(answer_choices[answer_index_list[0]][0])