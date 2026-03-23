from z3 import *

# Articles: G, H, J (finance); Q, R, S (nutrition); Y (wildlife)
articles = ["G", "H", "J", "Q", "R", "S", "Y"]
# Topic mapping
topic = {
    "G": 0, "H": 1, "J": 0,  # finance
    "Q": 2, "R": 2, "S": 2,   # nutrition
    "Y": 3                    # wildlife
}

# Position variables: pos[article] = position (1-7)
pos = {a: Int(f"pos_{a}") for a in articles}

# Base solver
solver = Solver()

# Domain constraints: positions 1-7, all distinct
for a in articles:
    solver.add(pos[a] >= 1, pos[a] <= 7)
solver.add(Distinct(*[pos[a] for a in articles]))

# Topic constraints: consecutive positions cannot have same topic
for i in range(1, 7):
    for j in range(i + 1, 8):
        # For each pair of articles a, b: if pos[a] = i and pos[b] = j where j = i+1, then topic(a) != topic(b)
        # Instead of checking all pairs, we can check for each position k (1-6), the articles at positions k and k+1 must have different topics
        # But since we don't know which articles are at positions k and k+1, we use a different approach:
        # For any two articles a, b: if topic(a) == topic(b), then |pos[a] - pos[b]| != 1
        pass

# Better approach: For each pair of articles with same topic, ensure they are not consecutive
for i in range(len(articles)):
    for j in range(i + 1, len(articles)):
        a, b = articles[i], articles[j]
        if topic[a] == topic[b]:
            solver.add(Abs(pos[a] - pos[b]) != 1)

# S–Q conditional constraint: S can be earlier than Q only if Q is third
# Equivalent to: (Q == 3) OR (S > Q)
solver.add(Or(pos["Q"] == 3, pos["S"] > pos["Q"]))

# S–Y constraint: S must be earlier than Y
solver.add(pos["S"] < pos["Y"])

# J–G–R chain: J < G and G < R
solver.add(pos["J"] < pos["G"])
solver.add(pos["G"] < pos["R"])

# Answer choices: ['H is fourth.', 'H is sixth.', 'R is fourth.', 'R is seventh.', 'Y is fifth.']
answer_choices = [
    ("H", 4),
    ("H", 6),
    ("R", 4),
    ("R", 7),
    ("Y", 5)
]

# Function to count models
def count_models(s, max_count=2):
    models = []
    while len(models) < max_count:
        if s.check() == unsat:
            break
        m = s.model()
        models.append(m)
        # Block this model
        block = Or([v() != m[v] for v in m.decls()])
        s.add(block)
    return len(models)

answer_index_list = []
for idx, (article, position) in enumerate(answer_choices):
    s_chk = Solver()
    # Add all base constraints
    for assertion in solver.assertions():
        s_chk.add(assertion)
    
    # Add constraint that the article is at the specified position
    s_chk.add(pos[article] == position)
    
    # Count models
    num_models = count_models(s_chk, max_count=2)
    
    if num_models == 1:
        answer_index_list.append(idx)

print(answer_index_list)