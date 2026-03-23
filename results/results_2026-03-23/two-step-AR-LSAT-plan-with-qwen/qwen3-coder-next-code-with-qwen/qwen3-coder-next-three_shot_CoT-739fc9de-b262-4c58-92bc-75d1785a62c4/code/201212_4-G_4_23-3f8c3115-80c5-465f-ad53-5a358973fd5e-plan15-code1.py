from z3 import *

# Articles
articles = ["G", "H", "J", "Q", "R", "S", "Y"]
pos = {a: Int(f"pos_{a}") for a in articles}

# Base solver
solver = Solver()

# Domain constraints: positions 1-7, all distinct
for a in articles:
    solver.add(pos[a] >= 1, pos[a] <= 7)
solver.add(Distinct(*[pos[a] for a in articles]))

# Topic groups
finance = {"G", "H", "J"}
nutrition = {"Q", "R", "S"}
wildlife = {"Y"}

# No consecutive same-topic constraint
for topic_group in [finance, nutrition]:
    articles_in_topic = list(topic_group)
    for i in range(len(articles_in_topic)):
        for j in range(i + 1, len(articles_in_topic)):
            a1, a2 = articles_in_topic[i], articles_in_topic[j]
            solver.add(Abs(pos[a1] - pos[a2]) != 1)

# S can be earlier than Q only if Q is third: (S < Q) → (Q == 3)
# Equivalent to: S >= Q or Q == 3
solver.add(Or(pos["S"] >= pos["Q"], pos["Q"] == 3))

# S before Y
solver.add(pos["S"] < pos["Y"])

# J < G < R
solver.add(pos["J"] < pos["G"])
solver.add(pos["G"] < pos["R"])

# Answer choices
answer_choices = [
    ("H is fourth.", lambda: pos["H"] == 4),
    ("H is sixth.", lambda: pos["H"] == 6),
    ("R is fourth.", lambda: pos["R"] == 4),
    ("R is seventh.", lambda: pos["R"] == 7),
    ("Y is fifth.", lambda: pos["Y"] == 5)
]

# Check each answer choice for uniqueness
answer_index_list = []
for idx, (desc, constraint_fn) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add the proposed condition
    s_chk.add(constraint_fn())
    
    if s_chk.check() == sat:
        # Count number of models
        models = []
        while s_chk.check() == sat:
            model = s_chk.model()
            # Create a constraint that blocks this exact assignment
            block = [pos[a] != model[pos[a]].as_long() for a in articles]
            s_chk.add(Or(block))
            models.append(model)
        
        if len(models) == 1:
            answer_index_list.append(idx)

print(answer_index_list)