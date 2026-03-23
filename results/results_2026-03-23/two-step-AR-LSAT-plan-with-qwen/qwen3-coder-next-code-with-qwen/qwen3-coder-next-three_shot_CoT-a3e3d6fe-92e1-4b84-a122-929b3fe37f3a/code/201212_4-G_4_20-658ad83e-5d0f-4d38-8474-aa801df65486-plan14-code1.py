from z3 import *

# Article indices: G, H, J (finance), Q, R, S (nutrition), Y (wildlife)
articles = ["G", "H", "J", "Q", "R", "S", "Y"]
finance = {"G", "H", "J"}
nutrition = {"Q", "R", "S"}
wildlife = {"Y"}

# Position variables: pos[article] = position (1-7)
pos = {a: Int(f"pos_{a}") for a in articles}

# Base solver
solver = Solver()

# Domain constraints: positions 1-7, all distinct
for a in articles:
    solver.add(pos[a] >= 1, pos[a] <= 7)
solver.add(Distinct(*[pos[a] for a in articles]))

# No consecutive same-topic constraint
for i in range(1, 7):  # positions 1-6 (i) and i+1
    for a in articles:
        for b in articles:
            if a != b and ((a in finance and b in finance) or 
                           (a in nutrition and b in nutrition)):
                solver.add(Or(pos[a] != i, pos[b] != i + 1))

# Conditional constraint: S can be earlier than Q only if Q is third
# Equivalent to: If S < Q then Q == 3, i.e., (S >= Q) OR (Q == 3)
solver.add(Or(pos["S"] >= pos["Q"], pos["Q"] == 3))

# S before Y constraint
solver.add(pos["S"] < pos["Y"])

# J < G < R chain
solver.add(pos["J"] < pos["G"])
solver.add(pos["G"] < pos["R"])

# Answer choices
answer_choices = [
    ("G is second", lambda: pos["G"] == 2),
    ("H is second", lambda: pos["H"] == 2),
    ("S is second", lambda: pos["S"] == 2),
    ("R is third", lambda: pos["R"] == 3),
    ("Y is third", lambda: pos["Y"] == 3)
]

# Check each answer choice
valid_indices = []
for idx, (desc, condition) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(condition())
    
    if s_chk.check() == sat:
        valid_indices.append(idx)

# Output the index of the first valid choice (as per LSAT format)
print(valid_indices[0] if valid_indices else -1)