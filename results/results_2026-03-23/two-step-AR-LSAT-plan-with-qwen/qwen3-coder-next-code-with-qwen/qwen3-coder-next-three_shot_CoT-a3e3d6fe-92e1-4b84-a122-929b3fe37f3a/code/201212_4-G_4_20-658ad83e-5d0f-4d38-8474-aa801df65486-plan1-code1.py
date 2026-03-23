from z3 import *

# Articles and their topics: F=fiance, N=nutrition, W=wildlife
articles = ["G", "H", "J", "Q", "R", "S", "Y"]
topic_map = {
    "G": 0, "H": 1, "J": 0,  # finance
    "Q": 2, "R": 2, "S": 2,   # nutrition
    "Y": 3                     # wildlife (use distinct value)
}

# Position variables for each article
pos = {a: Int(f"pos_{a}") for a in articles}

# Base solver
solver = Solver()

# Domain constraints: positions 1-7, all distinct
for a in articles:
    solver.add(pos[a] >= 1, pos[a] <= 7)
solver.add(Distinct(*[pos[a] for a in articles]))

# Consecutive articles cannot cover the same topic
# Create topic assignment function: for position k, get article at that position and its topic
# We'll use a piecewise approach: for each consecutive pair of positions (i, i+1),
# ensure no two articles at those positions have the same topic
for k in range(1, 7):
    # For each pair of articles (a, b), if pos[a] == k and pos[b] == k+1, then topic(a) != topic(b)
    # Instead of complex encoding, we'll enforce: for any two articles with same topic, they cannot be consecutive
    # But better: iterate over all pairs of articles and add constraint that if they are consecutive, topics differ
    # Simpler: for each pair of articles (a,b), if topic(a) == topic(b), then |pos[a] - pos[b]| != 1
    pass

# Actually, let's implement the consecutive constraint more directly:
# For each pair of articles with same topic, they cannot be adjacent
same_topic_pairs = []
for i in range(len(articles)):
    for j in range(i+1, len(articles)):
        a, b = articles[i], articles[j]
        if topic_map[a] == topic_map[b]:
            same_topic_pairs.append((a, b))

for a, b in same_topic_pairs:
    solver.add(Abs(pos[a] - pos[b]) != 1)

# S can be earlier than Q only if Q is third: (pos_S < pos_Q) -> (pos_Q == 3)
solver.add(Or(pos["S"] >= pos["Q"], pos["Q"] == 3))

# S must be earlier than Y
solver.add(pos["S"] < pos["Y"])

# J < G < R
solver.add(pos["J"] < pos["G"])
solver.add(pos["G"] < pos["R"])

# Answer choices
answer_choices = [
    ("G is second", lambda: pos["G"] == 2),
    ("H is second", lambda: pos["H"] == 2),
    ("S is second", lambda: pos["S"] == 2),
    ("R is third", lambda: pos["R"] == 3),
    ("Y is third", lambda: pos["Y"] == 3)
]

# Check each answer choice
answer_index_list = []
for idx, (desc, constraint) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    constraint()  # Add the specific constraint
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)