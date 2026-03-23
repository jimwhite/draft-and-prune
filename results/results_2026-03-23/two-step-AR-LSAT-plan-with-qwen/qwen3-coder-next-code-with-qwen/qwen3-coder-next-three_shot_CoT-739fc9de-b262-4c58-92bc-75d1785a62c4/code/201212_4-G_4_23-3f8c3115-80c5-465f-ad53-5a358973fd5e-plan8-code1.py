from z3 import *

# Articles
articles = ["G", "H", "J", "Q", "R", "S", "Y"]

# Position variables: pos[article] = position (1-7)
pos = {a: Int(f"pos_{a}") for a in articles}

# Base solver
solver = Solver()

# Domain constraints: positions 1-7, all distinct
for a in articles:
    solver.add(pos[a] >= 1, pos[a] <= 7)
solver.add(Distinct(*[pos[a] for a in articles]))

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

# No consecutive same-topic constraint
for i in range(1, 7):
    for j in range(i + 1, 8):
        # For each pair of articles, if they are at consecutive positions,
        # they must be different topics
        for a1 in articles:
            for a2 in articles:
                if topic[a1] == topic[a2]:
                    solver.add(Not(And(pos[a1] == i, pos[a2] == i + 1)))
                    solver.add(Not(And(pos[a1] == i + 1, pos[a2] == i)))

# Conditional constraint: S before Q implies Q is third
solver.add(Implies(pos["S"] < pos["Q"], pos["Q"] == 3))

# S before Y
solver.add(pos["S"] < pos["Y"])

# J before G, G before R
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

# Check each choice
answer_index_list = []
for idx, (desc, constraint) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add the fixed position constraint
    constraint()
    
    if s_chk.check() == unsat:
        continue  # Invalid
    
    # Count number of satisfying assignments
    models = []
    while s_chk.check() == sat:
        m = s_chk.model()
        # Record the model
        assignment = tuple(m[pos[a]].as_long() for a in articles)
        models.append(assignment)
        
        # Block this model
        s_chk.add(Or(*[pos[a] != m[pos[a]].as_long() for a in articles]))
    
    if len(models) == 1:
        answer_index_list.append(idx)

print(answer_index_list)