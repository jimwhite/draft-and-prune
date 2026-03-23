from z3 import *

# Article indices: G, H, J (finance); Q, R, S (nutrition); Y (wildlife)
articles = ["G", "H", "J", "Q", "R", "S", "Y"]
pos = {a: Int(f"pos_{a}") for a in articles}

# Base solver
solver = Solver()

# Domain constraints: positions 1-7, all distinct
for a in articles:
    solver.add(pos[a] >= 1, pos[a] <= 7)
solver.add(Distinct(*[pos[a] for a in articles]))

# Topic adjacency constraint: no two consecutive articles share same topic
topic = {
    "G": 0, "H": 0, "J": 0,  # finance
    "Q": 1, "R": 1, "S": 1,   # nutrition
    "Y": 2                    # wildlife
}

# For each pair of articles, if they are consecutive in the sequence, they must have different topics
# We'll add constraints for all adjacent positions: if article A is at position i and B at i+1, then topic(A) != topic(B)
# Instead of quantifiers, we'll use implications: for any two distinct articles A and B,
# if |pos[A] - pos[B]| == 1 then topic(A) != topic(B)
# This is complex with integers, so we use a different approach: for each pair of articles with same topic,
# they cannot be consecutive (i.e., |pos[A] - pos[B]| != 1)
for i in range(len(articles)):
    for j in range(i+1, len(articles)):
        a1, a2 = articles[i], articles[j]
        if topic[a1] == topic[a2]:
            solver.add(Abs(pos[a1] - pos[a2]) != 1)

# S before Q conditional: S < Q → Q is third
# Equivalent to: (S >= Q) OR (Q == 3)
solver.add(Or(pos["S"] >= pos["Q"], pos["Q"] == 3))

# S before Y: pos_S < pos_Y
solver.add(pos["S"] < pos["Y"])

# J before G, G before R: pos_J < pos_G < pos_R
solver.add(pos["J"] < pos["G"])
solver.add(pos["G"] < pos["R"])

# Answer choices: check which could be true (SAT)
answer_choices = [
    ("G is second", lambda p: p["G"] == 2),
    ("H is second", lambda p: p["H"] == 2),
    ("S is second", lambda p: p["S"] == 2),
    ("R is third", lambda p: p["R"] == 3),
    ("Y is third", lambda p: p["Y"] == 3)
]

answer_index_list = []
for idx, (desc, constraint) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    # Add the specific constraint for this choice
    s_chk.add(constraint(pos))
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)