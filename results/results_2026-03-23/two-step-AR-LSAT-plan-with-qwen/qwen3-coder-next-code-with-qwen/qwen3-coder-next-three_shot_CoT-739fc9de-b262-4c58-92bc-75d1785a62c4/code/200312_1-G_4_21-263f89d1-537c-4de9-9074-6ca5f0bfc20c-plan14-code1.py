from z3 import *

# Student indices: Jiang=0, Kramer=1, Lopez=2, Megregian=3, O'Neill=4
# Play indices: Sunset=0, Tamerlane=1, Undulation=2

r = [[Bool(f"r_{s}_{p}") for p in range(3)] for s in range(5)]

solver = Solver()

# At-least-one constraint: each student reviews at least one play
for s in range(5):
    solver.add(Or(r[s][0], r[s][1], r[s][2]))

# Kramer and Lopez each review fewer plays than Megregian
def count_reviews(student):
    return Sum([If(r[student][p], 1, 0) for p in range(3)])

solver.add(count_reviews(1) < count_reviews(3))  # Kramer < Megregian
solver.add(count_reviews(2) < count_reviews(3))  # Lopez < Megregian

# Neither Lopez nor Megregian reviews any play Jiang reviews
for p in range(3):
    solver.add(Implies(r[0][p], And(Not(r[2][p]), Not(r[3][p]))))

# Kramer and O'Neill both review Tamerlane (play 1)
solver.add(r[1][1] == True)
solver.add(r[4][1] == True)

# Exactly two students review exactly the same plays
# Create equality variables for each unordered pair (i, j), i < j
equality_vars = []
for i in range(5):
    for j in range(i + 1, 5):
        eq = Bool(f"eq_{i}_{j}")
        # eq is true iff students i and j have identical review sets
        solver.add(eq == And([r[i][p] == r[j][p] for p in range(3)]))
        equality_vars.append((eq, i, j))

# Exactly one pair has identical review sets
solver.add(Sum([If(eq, 1, 0) for eq, _, _ in equality_vars]) == 1)

# Given condition: exactly three students review Undulation (play 2)
solver.add(Sum([If(r[s][2], 1, 0) for s in range(5)]) == 3)

# Answer choices
answer_conditions = [
    Not(r[3][2]),      # A) Megregian does not review Undulation
    Not(r[4][2]),      # B) O'Neill does not review Undulation
    r[0][2],           # C) Jiang reviews Undulation
    r[2][1],           # D) Lopez reviews Tamerlane
    r[4][0]            # E) O'Neill reviews Sunset
]

answer_index_list = []
for idx, cond in enumerate(answer_conditions):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(cond)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)