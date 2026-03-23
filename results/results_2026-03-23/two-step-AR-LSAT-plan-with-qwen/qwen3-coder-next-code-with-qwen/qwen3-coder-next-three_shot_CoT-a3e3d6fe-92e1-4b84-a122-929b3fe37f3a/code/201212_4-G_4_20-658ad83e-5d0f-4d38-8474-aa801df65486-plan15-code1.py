from z3 import *

# Article indices: G=0, H=1, J=2, Q=3, R=4, S=5, Y=6
articles = ["G", "H", "J", "Q", "R", "S", "Y"]
topic_map = {
    "G": 0, "H": 0, "J": 0,   # Finance
    "Q": 1, "R": 1, "S": 1,   # Nutrition
    "Y": 2                    # Wildlife
}

# Position variables: pos[a] = position in sequence (1-7)
pos = {a: Int(f"pos_{a}") for a in articles}

# Base solver
solver = Solver()

# Domain constraints: positions 1-7 and all distinct
for a in articles:
    solver.add(pos[a] >= 1, pos[a] <= 7)
solver.add(Distinct(*[pos[a] for a in articles]))

# No consecutive same-topic constraint
for i, a1 in enumerate(articles):
    for j, a2 in enumerate(articles):
        if i < j and topic_map[a1] == topic_map[a2]:
            # Enforce |pos[a1] - pos[a2]| != 1
            solver.add(Or(pos[a1] < pos[a2] - 1, pos[a1] > pos[a2] + 1))

# S can be earlier than Q only if Q is third: (pos[S] < pos[Q]) → (pos[Q] == 3)
solver.add(Or(pos["S"] >= pos["Q"], pos["Q"] == 3))

# S must be earlier than Y
solver.add(pos["S"] < pos["Y"])

# J before G, and G before R
solver.add(pos["J"] < pos["G"])
solver.add(pos["G"] < pos["R"])

# Answer choices: check each possibility
answer_choices = [
    ("G is second", lambda s: s.add(pos["G"] == 2)),
    ("H is second.", lambda s: s.add(pos["H"] == 2)),
    ("S is second", lambda s: s.add(pos["S"] == 2)),
    ("R is third.", lambda s: s.add(pos["R"] == 3)),
    ("Y is third", lambda s: s.add(pos["Y"] == 3))
]

# Find which choices are possible
for idx, (desc, constraint) in enumerate(answer_choices):
    s_chk = Solver()
    # Add all base constraints
    for assertion in solver.assertions():
        s_chk.add(assertion)
    
    # Add the specific constraint for this choice
    constraint(s_chk)
    
    if s_chk.check() == sat:
        print(idx)
        break