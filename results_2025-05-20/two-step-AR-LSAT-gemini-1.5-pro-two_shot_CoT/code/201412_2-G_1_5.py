from z3 import *

# Define constants for musicians
G = 0
K = 1
P = 2
S = 3
T = 4
V = 5

# Define the solo order array
solo_order = Array('solo_order', IntSort(), IntSort())

# Create the solver
solver = Solver()

# Constraint 1: Domain
i = Int('i')
solver.add(ForAll(i, Implies(And(i >= 0, i <= 5), And(solo_order[i] >= 0, solo_order[i] <= 5))))

# Constraint 2: Distinctness
solver.add(Distinct([solo_order[i] for i in range(6)]))

# Constraint 3: Guitarist not 4th
solver.add(solo_order[3] != G)

# Constraint 4: Percussionist before Keyboard
solver.add(Exists(i, Exists(j, And(i < j, solo_order[i] == P, solo_order[j] == K, i >= 0, i <= 5, j >= 0, j <= 5))))

# Constraint 5: Violinist before Keyboard before Guitarist
solver.add(Exists(i, Exists(j, Exists(k, And(i < j, j < k, solo_order[i] == V, solo_order[j] == K, solo_order[k] == G, i >= 0, i <= 5, j >= 0, j <= 5, k >= 0, k <= 5))))

# Constraint 6: Saxophonist after P or T, not both
solver.add(Xor(
    Exists(i, Exists(j, And(i < j, solo_order[i] == P, solo_order[j] == S, i >= 0, i <= 5, j >= 0, j <= 5))),
    Exists(i, Exists(j, And(i < j, solo_order[i] == T, solo_order[j] == S, i >= 0, i <= 5, j >= 0, j <= 5)))
))

# Constraint 7: Violinist 4th
solver.add(solo_order[3] == V)

# Check answer choices
answers = [
    Not(Exists(i, And(i < 3, solo_order[i] == P, i >= 0, i <= 5))),
    Not(Exists(i, And(i < 3, solo_order[i] == T, i >= 0, i <= 5))),
    Not(Exists(i, Exists(j, And(i < j, solo_order[i] == T, solo_order[j] == G, i >= 0, i <= 5, j >= 0, j <= 5)))),
    Not(Exists(i, And(i < 3, solo_order[i] == S, i >= 0, i <= 5))),
    Not(Exists(i, Exists(j, And(i < j, solo_order[i] == T, solo_order[j] == S, i >= 0, i <= 5, j >= 0, j <= 5))))
]

for i, answer in enumerate(answers):
    solver.push()
    solver.add(answer)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
