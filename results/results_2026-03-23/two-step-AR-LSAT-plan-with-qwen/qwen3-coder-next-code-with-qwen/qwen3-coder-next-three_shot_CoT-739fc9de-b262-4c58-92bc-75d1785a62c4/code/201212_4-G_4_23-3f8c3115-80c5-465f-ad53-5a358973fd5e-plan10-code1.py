from z3 import *

# Articles and their topics
articles = ["G", "H", "J", "Q", "R", "S", "Y"]
finance = {"G", "H", "J"}
nutrition = {"Q", "R", "S"}
wildlife = {"Y"}

def get_topic(article):
    if article in finance:
        return "finance"
    elif article in nutrition:
        return "nutrition"
    else:
        return "wildlife"

# Position variables (0-based)
pos = {a: Int(f"pos_{a}") for a in articles}

# Base solver
solver = Solver()

# Domain constraints: positions 0-6, all distinct
for a in articles:
    solver.add(pos[a] >= 0, pos[a] <= 6)
solver.add(Distinct(*[pos[a] for a in articles]))

# Consecutive articles cannot cover the same topic
for i, a1 in enumerate(articles):
    for j, a2 in enumerate(articles):
        if i < j:
            # If |pos[a1] - pos[a2]| == 1, then topics must differ
            # This is equivalent to: if same topic, then |pos[a1] - pos[a2]| != 1
            if get_topic(a1) == get_topic(a2):
                solver.add(Abs(pos[a1] - pos[a2]) != 1)

# S can be earlier than Q only if Q is third (0-based: Q == 2)
# S < Q → Q == 2, equivalent to: S < Q implies Q == 2
# Which is logically: Not(S < Q) OR (Q == 2)
solver.add(Or(pos["S"] >= pos["Q"], pos["Q"] == 2))

# S must be earlier than Y
solver.add(pos["S"] < pos["Y"])

# J before G, and G before R
solver.add(pos["J"] < pos["G"])
solver.add(pos["G"] < pos["R"])

# Answer choices
answer_choices = [
    ("H is fourth.", lambda s: s.add(pos["H"] == 3)),
    ("H is sixth.", lambda s: s.add(pos["H"] == 5)),
    ("R is fourth.", lambda s: s.add(pos["R"] == 3)),
    ("R is seventh.", lambda s: s.add(pos["R"] == 6)),
    ("Y is fifth.", lambda s: s.add(pos["Y"] == 4))
]

answer_index_list = []

for idx, (desc, constraint_fn) in enumerate(answer_choices):
    # Clone base solver
    s_base = Solver()
    s_base.add(solver.assertions())
    
    # Add choice constraint
    constraint_fn(s_base)
    
    if s_base.check() == unsat:
        # No solution at all, so not fully determined
        continue
    
    # Get first model
    model = s_base.model()
    
    # Create assignment dictionary
    assignment = {}
    for a in articles:
        val = model.eval(pos[a])
        if is_int(val):
            assignment[a] = val.as_long()
        else:
            assignment[a] = int(str(val))
    
    # Check uniqueness: add constraint that at least one position differs
    s_unique = Solver()
    s_unique.add(solver.assertions())
    constraint_fn(s_unique)
    
    # Add constraint that at least one article has different position
    diff_constraint = Or([pos[a] != assignment[a] for a in articles])
    s_unique.add(diff_constraint)
    
    if s_unique.check() == unsat:
        # Original SAT, uniqueness check UNSAT => unique solution
        answer_index_list.append(idx)

print(answer_index_list)