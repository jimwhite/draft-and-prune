from z3 import *

# Articles: G, H, J (finance); Q, R, S (nutrition); Y (wildlife)
articles = ["G", "H", "J", "Q", "R", "S", "Y"]

# Topic mapping
topic = {
    "G": 0,  # finance
    "H": 0,  # finance
    "J": 0,  # finance
    "Q": 1,  # nutrition
    "R": 1,  # nutrition
    "S": 1,  # nutrition
    "Y": 2   # wildlife
}

# Position variables: pos[article] = position (1-7)
pos = {a: Int(f"pos_{a}") for a in articles}

# Base solver
solver = Solver()

# Distinctness constraint: all positions are distinct and in [1,7]
solver.add(Distinct(*[pos[a] for a in articles]))
for a in articles:
    solver.add(pos[a] >= 1, pos[a] <= 7)

# No consecutive same-topic constraint
for i in range(len(articles)):
    for j in range(i + 1, len(articles)):
        a1, a2 = articles[i], articles[j]
        # If two articles are consecutive (|pos[a1] - pos[a2]| == 1), they must have different topics
        solver.add(Implies(Abs(pos[a1] - pos[a2]) == 1, topic[a1] != topic[a2]))

# Conditional constraint: S earlier than Q only if Q is third
# (pos_S < pos_Q) → (pos_Q == 3)
solver.add(Implies(pos["S"] < pos["Q"], pos["Q"] == 3))

# S before Y constraint
solver.add(pos["S"] < pos["Y"])

# J–G–R chain constraint: J before G, G before R
solver.add(pos["J"] < pos["G"])
solver.add(pos["G"] < pos["R"])

# Answer choices: each choice asserts a specific article is in a specific position
answer_choices = [
    ("G", 2),   # G is second
    ("H", 2),   # H is second
    ("S", 2),   # S is second
    ("R", 3),   # R is third
    ("Y", 3)    # Y is third
]

# Check each answer choice
answer_index_list = []
for idx, (article, position) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert the article is in the specified position
    s_chk.add(pos[article] == position)
    
    # If SAT, this choice could be true
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)