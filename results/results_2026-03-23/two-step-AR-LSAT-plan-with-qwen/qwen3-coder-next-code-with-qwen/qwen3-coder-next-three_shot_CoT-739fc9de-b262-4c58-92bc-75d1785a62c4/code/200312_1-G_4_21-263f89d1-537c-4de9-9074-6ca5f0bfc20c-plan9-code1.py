from z3 import *

# Student indices: Jiang=0, Kramer=1, Lopez=2, Megregian=3, O'Neill=4
# Play indices: Sunset=0, Tamerlane=1, Undulation=2

review = [[Bool(f"review_{i}_{j}") for j in range(3)] for i in range(5)]

solver = Solver()

# Each student reviews at least one play
for i in range(5):
    solver.add(Or(review[i][0], review[i][1], review[i][2]))

# Kramer and Lopez each review fewer plays than Megregian
def count_reviews(student):
    return Sum([If(review[student][j], 1, 0) for j in range(3)])

solver.add(count_reviews(1) < count_reviews(3))
solver.add(count_reviews(2) < count_reviews(3))

# Neither Lopez nor Megregian reviews any play Jiang reviews
for j in range(3):
    solver.add(Implies(review[2][j], Not(review[0][j])))
    solver.add(Implies(review[3][j], Not(review[0][j])))

# Kramer and O'Neill both review Tamerlane
solver.add(review[1][1] == True)
solver.add(review[4][1] == True)

# Exactly two students review the same set of plays
eq = {}
for i in range(5):
    for j in range(i+1, 5):
        eq[(i,j)] = And(
            review[i][0] == review[j][0],
            review[i][1] == review[j][1],
            review[i][2] == review[j][2]
        )

# At least one pair is equal
at_least_one = Or([eq[(i,j)] for i in range(5) for j in range(i+1, 5)])
solver.add(at_least_one)

# At most one pair is equal
for (i1,j1) in eq:
    for (i2,j2) in eq:
        if (i1 < i2) or (i1 == i2 and j1 < j2):
            if (i1,j1) != (i2,j2):
                solver.add(Not(And(eq[(i1,j1)], eq[(i2,j2)])))

# Exactly three students review Undulation
solver.add(Sum([If(review[i][2], 1, 0) for i in range(5)]) == 3)

# Answer choices
answer_choices = [
    Not(review[3][2]),      # Megregian does not review Undulation
    Not(review[4][2]),      # O'Neill does not review Undulation
    review[0][2],           # Jiang reviews Undulation
    review[2][1],           # Lopez reviews Tamerlane
    review[4][0]            # O'Neill reviews Sunset
]

# Check each answer choice
answer_index_list = []
for idx, cond in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(cond)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)