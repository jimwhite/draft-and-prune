from z3 import *

# Article indices: G, H, J (finance); Q, R, S (nutrition); Y (wildlife)
articles = ["G", "H", "J", "Q", "R", "S", "Y"]
# Topic mapping: 0=finance, 1=nutrition, 2=wildlife
topic = {"G": 0, "H": 1, "J": 0, "Q": 1, "R": 1, "S": 1, "Y": 2}

# Position variables: pos[article] = position (1-7)
pos = {a: Int(f"pos_{a}") for a in articles}

# Base solver
solver = Solver()

# Domain constraints: positions 1-7 and all distinct
for a in articles:
    solver.add(pos[a] >= 1, pos[a] <= 7)
solver.add(Distinct(*[pos[a] for a in articles]))

# Topic-consecutive-different constraint: same-topic articles must be at least 2 positions apart
same_topic_pairs = []
for i, a1 in enumerate(articles):
    for j, a2 in enumerate(articles):
        if i < j and topic[a1] == topic[a2]:
            same_topic_pairs.append((a1, a2))

for a1, a2 in same_topic_pairs:
    solver.add(Abs(pos[a1] - pos[a2]) >= 2)

# S can be earlier than Q only if Q is third: (pos[S] < pos[Q]) → (pos[Q] == 3)
solver.add(Implies(pos["S"] < pos["Q"], pos["Q"] == 3))

# S must be earlier than Y
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

# Check each answer choice
answer_index_list = []
for idx, (desc, constraint_fn) in enumerate(answer_choices):
    # Clone base solver and add the condition
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(constraint_fn())
    
    # Check if SAT
    if s_chk.check() == unsat:
        continue  # Skip if no solution exists
    
    # Get the model
    m = s_chk.model()
    
    # Extract positions from model
    assignment = {a: m.eval(pos[a]).as_long() for a in articles}
    
    # Check uniqueness: try to find another solution that differs
    s_unique = Solver()
    s_unique.add(solver.assertions())
    s_unique.add(constraint_fn())
    
    # Add constraint that at least one article has a different position
    diff_constraint = Or(*[pos[a] != assignment[a] for a in articles])
    s_unique.add(diff_constraint)
    
    # If this is UNSAT, then the original solution is unique
    if s_unique.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)