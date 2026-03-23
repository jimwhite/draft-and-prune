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

# Topic groupings: Finance={G,H,J}, Nutrition={Q,R,S}, Wildlife={Y}
def topic(i):
    if i in [0, 1, 2]:  # G, H, J
        return 0  # Finance
    elif i in [3, 4, 5]:  # Q, R, S
        return 1  # Nutrition
    else:  # Y (index 6)
        return 2  # Wildlife

# No consecutive same-topic constraint
for i in range(7):
    for j in range(i + 1, 7):
        solver.add(
            Implies(Abs(pos[i] - pos[j]) == 1, topic(i) != topic(j))
        )

# S before Q conditional: If S < Q then Q must be 3rd
solver.add(Implies(pos[5] < pos[3], pos[3] == 3))

# S before Y
solver.add(pos[5] < pos[6])

# J before G and G before R
solver.add(pos[0] < pos[2])  # J before G? Wait, J is index 2, G is index 0
# Correction: J before G means pos[J] < pos[G], i.e., pos[2] < pos[0]
solver.add(pos[2] < pos[0])  # J before G
solver.add(pos[0] < pos[4])  # G before R

# Answer choices: 
# ['G is second', 'H is second.', 'S is second', 'R is third.', 'Y is third']
# G=0, H=1, S=5, R=4, Y=6
answer_choices = [
    (0, 2),  # G is second: pos[0] == 2
    (1, 2),  # H is second: pos[1] == 2
    (5, 2),  # S is second: pos[5] == 2
    (4, 3),  # R is third: pos[4] == 3
    (6, 3)   # Y is third: pos[6] == 3
]

answer_index_list = []
for idx, (article_idx, position) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert the position condition
    s_chk.add(pos[article_idx] == position)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)