from z3 import *

# Articles
articles = ["G", "H", "J", "Q", "R", "S", "Y"]

# Position variables: pos[article] = position (1-7)
pos = {a: Int(f"pos_{a}") for a in articles}

# Base solver
solver = Solver()

# Domain constraints: each position between 1 and 7, all distinct
for a in articles:
    solver.add(pos[a] >= 1, pos[a] <= 7)
solver.add(Distinct(*[pos[a] for a in articles]))

# Topic categories
def topic(a):
    if a in ["G", "H", "J"]:
        return 0  # finance
    elif a in ["Q", "R", "S"]:
        return 1  # nutrition
    else:  # a == "Y"
        return 2  # wildlife

# Consecutive articles cannot cover the same topic
for i in range(1, 7):
    for j in range(i + 1, 8):
        # For each pair of positions (i, j), if they are consecutive, articles must differ in topic
        # Instead of checking all pairs, we'll use a different approach: for each position k from 1 to 6,
        # find which articles are at positions k and k+1, then enforce they have different topics
        pass

# Better approach: use permutation constraints implicitly via distinct positions and topic checks
# We'll add constraints for each possible consecutive position pair (1,2), (2,3), ..., (6,7)
# For each such pair of positions, if article X is at position k and article Y is at position k+1,
# then topic(X) != topic(Y). To handle this, we'll use a standard trick: for each consecutive position pair,
# add constraints that no two articles at those positions have the same topic.

# For each consecutive position pair (k, k+1), add constraint that if article a is at k and article b is at k+1,
# then topic(a) != topic(b). We can express this as: for all articles a, b, if pos[a] = k and pos[b] = k+1 then topic(a) != topic(b)
# Instead, we'll use: for each article pair (a,b), if they have the same topic, then |pos[a] - pos[b]| != 1
# But that's complex. Better: for each consecutive position pair, add constraints using implications.

# Alternative standard approach: For each article a and b with same topic, add constraint that they are not consecutive
for i in range(len(articles)):
    for j in range(i + 1, len(articles)):
        a = articles[i]
        b = articles[j]
        if topic(a) == topic(b):
            solver.add(Abs(pos[a] - pos[b]) != 1)

# S can be earlier than Q only if Q is third: (pos_S < pos_Q) → (pos_Q == 3)
solver.add(Implies(pos["S"] < pos["Q"], pos["Q"] == 3))

# S must be earlier than Y
solver.add(pos["S"] < pos["Y"])

# J before G, G before R
solver.add(pos["J"] < pos["G"])
solver.add(pos["G"] < pos["R"])

# Answer choices: check which could be true
answer_choices = [
    ("G is second", lambda: pos["G"] == 2),
    ("H is second.", lambda: pos["H"] == 2),
    ("S is second", lambda: pos["S"] == 2),
    ("R is third.", lambda: pos["R"] == 3),
    ("Y is third", lambda: pos["Y"] == 3)
]

answer_index_list = []
for idx, (desc, constraint) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(constraint())
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)