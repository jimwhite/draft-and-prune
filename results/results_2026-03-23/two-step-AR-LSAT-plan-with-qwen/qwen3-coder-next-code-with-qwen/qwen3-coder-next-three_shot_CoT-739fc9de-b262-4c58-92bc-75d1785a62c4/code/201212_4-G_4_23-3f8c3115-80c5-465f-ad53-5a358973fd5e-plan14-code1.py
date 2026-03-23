from z3 import *

# Article indices
articles = ["G", "H", "J", "Q", "R", "S", "Y"]
# Topic mapping
topics = {
    "G": 0, "H": 0, "J": 0,  # finance
    "Q": 1, "R": 1, "S": 1,   # nutrition
    "Y": 2                    # wildlife
}

# Position variables: pos[article] = position (1-7)
pos = {a: Int(f"pos_{a}") for a in articles}

# Base solver
solver = Solver()

# Domain constraints: positions 1-7
for a in articles:
    solver.add(pos[a] >= 1, pos[a] <= 7)

# All-different constraint
solver.add(Distinct(*[pos[a] for a in articles]))

# Topic adjacency constraint: consecutive positions cannot have same topic
for i in range(1, 7):
    for j in range(i + 1, 8):
        # For each pair of articles a and b, if |pos[a] - pos[b]| == 1 then topics must differ
        # We'll encode this as: for each pair of articles, if they are consecutive positions, topics differ
        # Instead, we'll use a more direct approach: for each pair of articles (a,b), if they are adjacent in the sequence, topics differ
        # But since we don't know which articles are adjacent, we'll use implication:
        # For any two distinct articles a and b: if |pos[a] - pos[b]| == 1, then topics[a] != topics[b]
        # This is equivalent to: for any two articles a and b with same topic, |pos[a] - pos[b]| != 1
        pass

# Better approach: for each pair of articles with same topic, ensure they are not consecutive
for i in range(len(articles)):
    for j in range(i + 1, len(articles)):
        a1, a2 = articles[i], articles[j]
        if topics[a1] == topics[a2]:
            solver.add(Abs(pos[a1] - pos[a2]) != 1)

# S before Q only if Q is third: (pos[S] < pos[Q]) -> (pos[Q] == 3)
solver.add(Implies(pos["S"] < pos["Q"], pos["Q"] == 3))

# S before Y
solver.add(pos["S"] < pos["Y"])

# J before G and G before R
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

# Check each choice for uniqueness
answer_index_list = []
for idx, (desc, condition) in enumerate(answer_choices):
    s_chk = Solver()
    # Add base constraints
    for a in solver.assertions():
        s_chk.add(a)
    
    # Add condition from choice
    s_chk.add(condition())
    
    if s_chk.check() == sat:
        # Get the model
        m = s_chk.model()
        
        # Create constraint that at least one position differs from this model
        diff_constraint = Or(*[pos[a] != m.eval(pos[a]).as_long() for a in articles])
        
        s_unique = Solver()
        # Add base constraints
        for a in solver.assertions():
            s_unique.add(a)
        # Add condition from choice
        s_unique.add(condition())
        # Add constraint that solution is different from current model
        s_unique.add(diff_constraint)
        
        if s_unique.check() == unsat:
            # Unique solution found
            answer_index_list.append(idx)

print(answer_index_list)