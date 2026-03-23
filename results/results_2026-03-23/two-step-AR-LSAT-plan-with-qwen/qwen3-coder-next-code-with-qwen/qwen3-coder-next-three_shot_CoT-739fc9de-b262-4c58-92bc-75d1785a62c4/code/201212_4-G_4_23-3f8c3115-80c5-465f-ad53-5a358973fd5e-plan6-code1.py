from z3 import *

# Articles and their topics
articles = ["G", "H", "J", "Q", "R", "S", "Y"]
topic = {
    "G": 0, "H": 0, "J": 0,  # Finance
    "Q": 1, "R": 1, "S": 1,  # Nutrition
    "Y": 2                   # Wildlife
}

# Position variables: pos[article] = position (1-7)
pos = {a: Int(f"pos_{a}") for a in articles}

# Base solver
solver = Solver()

# Domain constraints: positions 1-7, all distinct
for a in articles:
    solver.add(pos[a] >= 1, pos[a] <= 7)
solver.add(Distinct(*[pos[a] for a in articles]))

# No consecutive same-topic constraint
for i, a1 in enumerate(articles):
    for j, a2 in enumerate(articles):
        if i < j and topic[a1] == topic[a2]:
            solver.add(Abs(pos[a1] - pos[a2]) != 1)

# S before Q only if Q is third: (pos_S < pos_Q) → (pos_Q == 3)
# Equivalent to: (pos_S >= pos_Q) OR (pos_Q == 3)
solver.add(Or(pos["S"] >= pos["Q"], pos["Q"] == 3))

# S before Y
solver.add(pos["S"] < pos["Y"])

# J before G, G before R
solver.add(pos["J"] < pos["G"])
solver.add(pos["G"] < pos["R"])

# Answer choices: (article, position)
answer_choices = [
    ("H", 4),
    ("H", 6),
    ("R", 4),
    ("R", 7),
    ("Y", 5)
]

# Check each answer choice for uniqueness
answer_index_list = []
for idx, (article, position) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Fix the article at the given position
    s_chk.add(pos[article] == position)
    
    # Check if at least one solution exists
    if s_chk.check() == unsat:
        continue  # Skip if no solution
    
    # Count solutions: try to find a second distinct solution
    model = s_chk.model()
    # Block this first solution by adding constraint that at least one position differs
    block = []
    for a in articles:
        val = model.eval(pos[a]).as_long()
        block.append(pos[a] != val)
    s_chk.add(Or(block))
    
    # Check if a second solution exists
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)