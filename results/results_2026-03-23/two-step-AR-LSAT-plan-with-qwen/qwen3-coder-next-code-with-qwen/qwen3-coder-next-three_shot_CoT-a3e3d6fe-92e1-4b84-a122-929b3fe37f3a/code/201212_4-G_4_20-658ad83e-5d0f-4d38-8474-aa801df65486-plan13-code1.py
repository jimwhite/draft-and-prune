from z3 import *

# Articles
articles = ["G", "H", "J", "Q", "R", "S", "Y"]

# Position variables
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
for i, a1 in enumerate(articles):
    for j, a2 in enumerate(articles):
        if i < j:
            # Check if same topic
            topic1 = "finance" if a1 in finance else ("nutrition" if a1 in nutrition else "wildlife")
            topic2 = "finance" if a2 in finance else ("nutrition" if a2 in nutrition else "wildlife")
            if topic1 == topic2:
                solver.add(Abs(pos[a1] - pos[a2]) != 1)

# Conditional S before Q constraint: (pos[S] < pos[Q]) → (pos[Q] == 3)
solver.add(Or(pos["S"] >= pos["Q"], pos["Q"] == 3))

# S before Y constraint
solver.add(pos["S"] < pos["Y"])

# J before G, G before R chain
solver.add(pos["J"] < pos["G"])
solver.add(pos["G"] < pos["R"])

# Answer choices
answer_choices = [
    ("G", 2),
    ("H", 2),
    ("S", 2),
    ("R", 3),
    ("Y", 3)
]

# Check each answer choice
answer_index_list = []
for idx, (article, position) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert the position constraint
    s_chk.add(pos[article] == position)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)