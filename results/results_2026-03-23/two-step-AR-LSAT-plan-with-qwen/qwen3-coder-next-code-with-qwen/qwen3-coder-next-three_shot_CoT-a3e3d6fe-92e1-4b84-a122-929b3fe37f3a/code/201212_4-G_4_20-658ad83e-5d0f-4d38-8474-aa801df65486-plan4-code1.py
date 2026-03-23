from z3 import *

# Articles: G, H, J (finance); Q, R, S (nutrition); Y (wildlife)
articles = ["G", "H", "J", "Q", "R", "S", "Y"]

# Topic mapping: 0=finance, 1=nutrition, 2=wildlife
topic_map = {
    "G": 0, "H": 0, "J": 0,
    "Q": 1, "R": 1, "S": 1,
    "Y": 2
}

# Position variables: pos[article] = position (1-7)
pos = {a: Int(f"pos_{a}") for a in articles}

# Base solver
solver = Solver()

# Domain constraints: positions 1-7, all distinct
for a in articles:
    solver.add(pos[a] >= 1, pos[a] <= 7)
solver.add(Distinct(*[pos[a] for a in articles]))

# Topic adjacency constraint: consecutive positions must have different topics
for i in range(1, 7):
    for j in range(i + 1, 8):
        # For each pair of articles a, b: if pos[a] == i and pos[b] == j and |i-j|==1, then topics differ
        # Instead, we check all adjacent position pairs directly:
        pass

# Better approach: for each pair of articles, if their positions are consecutive, topics must differ
for a in articles:
    for b in articles:
        if a != b:
            # If |pos[a] - pos[b]| == 1, then topic_map[a] != topic_map[b]
            solver.add(Implies(Abs(pos[a] - pos[b]) == 1, topic_map[a] != topic_map[b]))

# S–Q conditional constraint: (S earlier than Q) → (Q is third)
solver.add(Implies(pos["S"] < pos["Q"], pos["Q"] == 3))

# S–Y ordering constraint: S before Y
solver.add(pos["S"] < pos["Y"])

# J–G–R chaining constraint: J before G before R
solver.add(pos["J"] < pos["G"])
solver.add(pos["G"] < pos["R"])

# Answer choices: check which could be true
answer_choices = [
    ("G is second", lambda p: p["G"] == 2),
    ("H is second.", lambda p: p["H"] == 2),
    ("S is second", lambda p: p["S"] == 2),
    ("R is third.", lambda p: p["R"] == 3),
    ("Y is third", lambda p: p["Y"] == 3)
]

answer_index_list = []
for idx, (desc, condition) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add the condition for this answer choice
    s_chk.add(condition(pos))
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)