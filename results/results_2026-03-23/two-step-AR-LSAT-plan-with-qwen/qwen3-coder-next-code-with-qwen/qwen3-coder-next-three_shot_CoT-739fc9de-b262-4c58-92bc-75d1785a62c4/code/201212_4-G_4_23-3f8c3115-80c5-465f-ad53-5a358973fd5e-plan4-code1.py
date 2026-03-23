from z3 import *

# Articles: G, H, J (finance); Q, R, S (nutrition); Y (wildlife)
articles = ["G", "H", "J", "Q", "R", "S", "Y"]

# Topic mapping
topic_map = {
    "G": 0, "H": 1, "J": 0,  # finance
    "Q": 2, "R": 2, "S": 2,   # nutrition
    "Y": 3                    # wildlife (distinct from others)
}

# Position variables: pos[article] = position in sequence (1-7)
pos = {a: Int(f"pos_{a}") for a in articles}

# Base solver
solver = Solver()

# Domain constraints: positions 1-7, all distinct
for a in articles:
    solver.add(pos[a] >= 1, pos[a] <= 7)
solver.add(Distinct(*[pos[a] for a in articles]))

# Consecutive articles cannot cover the same topic
for i in range(1, 7):
    for a in articles:
        for b in articles:
            if a != b and topic_map[a] == topic_map[b]:
                # If both have same topic, they cannot be consecutive
                solver.add(Not(And(pos[a] == i, pos[b] == i+1)))
                solver.add(Not(And(pos[a] == i+1, pos[b] == i)))

# Conditional constraint: S can be earlier than Q only if Q is third
# Equivalent: If pos[S] < pos[Q], then pos[Q] == 3
solver.add(Implies(pos["S"] < pos["Q"], pos["Q"] == 3))

# S must be earlier than Y
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

# Count solutions for each choice
def count_solutions(condition_expr):
    s = Solver()
    s.add(solver.assertions())
    s.add(condition_expr)
    
    models = []
    while s.check() == sat:
        m = s.model()
        models.append(m)
        # Block this model
        block = []
        for a in articles:
            val = m.eval(pos[a])
            if val is not None:
                block.append(pos[a] != val)
        s.add(Or(block))
    return len(models)

# Find choices that yield exactly one solution
answer_index_list = []
for idx, (desc, cond_func) in enumerate(answer_choices):
    count = count_solutions(cond_func())
    if count == 1:
        answer_index_list.append(idx)

print(answer_index_list)