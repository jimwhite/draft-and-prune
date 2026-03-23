from z3 import *

# Article variables: G, H, J (finance); Q, R, S (nutrition); Y (wildlife)
articles = ["G", "H", "J", "Q", "R", "S", "Y"]
pos = {a: Int(f"pos_{a}") for a in articles}

# Base solver
solver = Solver()

# Domain constraints: positions 1-7, all distinct
for a in articles:
    solver.add(pos[a] >= 1, pos[a] <= 7)
solver.add(Distinct(*[pos[a] for a in articles]))

# Topic mapping: finance=0, nutrition=1, wildlife=2
topic = {
    "G": 0, "H": 0, "J": 0,
    "Q": 1, "R": 1, "S": 1,
    "Y": 2
}

# No consecutive same topic constraint
for i in range(1, 7):
    for j in range(i + 1, 8):
        # For each pair of positions i and i+1, find articles at those positions
        # Instead, we'll add constraints for adjacent positions using implications
        pass

# Better approach: For each position pair (k, k+1), ensure different topics
for k in range(1, 7):
    # Create helper variables for each article being at position k and k+1
    # But Z3 doesn't support quantifiers easily, so we enumerate all pairs of articles
    for a1 in articles:
        for a2 in articles:
            if topic[a1] == topic[a2]:
                solver.add(Or(pos[a1] != k, pos[a2] != k + 1))

# S before Q only if Q is third: (S < Q) → (Q == 3)
# Equivalent to: (S >= Q) OR (Q == 3)
solver.add(Or(pos["S"] >= pos["Q"], pos["Q"] == 3))

# S before Y
solver.add(pos["S"] < pos["Y"])

# J before G, G before R
solver.add(pos["J"] < pos["G"])
solver.add(pos["G"] < pos["R"])

# Answer choices
answer_choices = [
    "H is fourth",   # pos_H == 4
    "H is sixth",    # pos_H == 6
    "R is fourth",   # pos_R == 4
    "R is seventh",  # pos_R == 7
    "Y is fifth"     # pos_Y == 5
]

answer_index_list = []

for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add the specific constraint from the choice
    if "fourth" in choice:
        article = "H" if "H" in choice else "R"
        s_chk.add(pos[article] == 4)
    elif "sixth" in choice:
        s_chk.add(pos["H"] == 6)
    elif "seventh" in choice:
        s_chk.add(pos["R"] == 7)
    elif "fifth" in choice:
        s_chk.add(pos["Y"] == 5)
    
    # Check if model exists
    if s_chk.check() == unsat:
        continue  # This choice is impossible
    
    # Get the first model
    model = s_chk.model()
    
    # Create constraint to exclude this model
    exclude_constraint = []
    for a in articles:
        val = model.eval(pos[a])
        exclude_constraint.append(pos[a] != val)
    s_chk.add(Or(*exclude_constraint))
    
    # Check if there's a second model
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)