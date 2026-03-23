from z3 import *

# Article position variables: pos[article] = position (1-7)
articles = ["G", "H", "J", "Q", "R", "S", "Y"]
pos = {a: Int(f"pos_{a}") for a in articles}

# Base solver
solver = Solver()

# Domain constraints: each article has a unique position from 1 to 7
for a in articles:
    solver.add(pos[a] >= 1, pos[a] <= 7)
solver.add(Distinct(*[pos[a] for a in articles]))

# Topic assignments
topic = {
    "G": 0, "H": 1, "J": 2,  # finance
    "Q": 3, "R": 4, "S": 5,   # nutrition
    "Y": 6                    # wildlife
}

# Consecutive articles cannot cover the same topic
for i in range(1, 7):
    for a1 in articles:
        for a2 in articles:
            if a1 != a2 and topic[a1] == topic[a2]:
                # If two articles have same topic, they cannot be consecutive
                solver.add(Or(pos[a1] != i, pos[a2] != i + 1))
                solver.add(Or(pos[a1] != i + 1, pos[a2] != i))

# S can be earlier than Q only if Q is third: (S_pos < Q_pos) → (Q_pos == 3)
# Equivalent to: S_pos >= Q_pos OR Q_pos == 3
solver.add(Or(pos["S"] >= pos["Q"], pos["Q"] == 3))

# S must be earlier than Y: S_pos < Y_pos
solver.add(pos["S"] < pos["Y"])

# J must be earlier than G, and G must be earlier than R: J < G < R
solver.add(pos["J"] < pos["G"])
solver.add(pos["G"] < pos["R"])

# Answer choices: check which could be true
answer_choices = [
    ("G is second", lambda: pos["G"] == 2),
    ("H is second.", lambda: pos["H"] == 2),
    ("S is second", lambda: pos["S"] == 2),
    ("R is third.", lambda: pos["R"] == 3),
    ("Y is third", lambda: pos["Y"] == 3)
]

# Check each choice
answer_index_list = []
for idx, (desc, constraint) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    constraint()  # Add the specific position constraint
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)