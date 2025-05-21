from z3 import *

# Define variables
solo_order = Array('solo_order', IntSort(), IntSort())

# Create solver and add constraints
solver = Solver()

# Constraint 1: Distinctness
solver.add(Distinct([solo_order[i] for i in range(6)]))

# Constraint 2: Guitarist not 4th
solver.add(solo_order[3] != 0)

# Constraint 3: Percussionist before Keyboard player
i = Int('i')
j = Int('j')
solver.add(ForAll([i, j], Implies(And(solo_order[i] == 2, solo_order[j] == 1, 0 <= i, i < 6, 0 <= j, j < 6), i < j)))

# Constraint 4: Violinist before Keyboard player
k = Int('k')
l = Int('l')
solver.add(ForAll([k, l], Implies(And(solo_order[k] == 5, solo_order[l] == 1, 0 <= k, k < 6, 0 <= l, l < 6), k < l)))

# Constraint 5: Keyboard player before Guitarist
m = Int('m')
n = Int('n')
solver.add(ForAll([m, n], Implies(And(solo_order[m] == 1, solo_order[n] == 0, 0 <= m, m < 6, 0 <= n, n < 6), m < n)))

# Constraint 6: Saxophonist after Percussionist or Trumpeter, not both
p = Int('p')
q = Int('q')
r = Int('r')
s = Int('s')
S_after_P = Exists([p, q], And(solo_order[p] == 3, solo_order[q] == 2, p > q, 0 <= p, p < 6, 0 <= q, q < 6))
S_after_T = Exists([r, s], And(solo_order[r] == 3, solo_order[s] == 4, r > s, 0 <= r, r < 6, 0 <= s, s < 6))
solver.add(Xor(S_after_P, S_after_T))

# Answer choices
choices = [
    [5, 2, 3, 0, 4, 1],  # A
    [2, 5, 1, 4, 3, 0],  # B
    [5, 4, 3, 2, 1, 0],  # C
    [1, 4, 5, 3, 0, 2],  # D
    [0, 5, 1, 2, 3, 4]   # E
]

# Check each answer choice
for i, choice in enumerate(choices):
    solver.push()
    for j in range(6):
        solver.add(solo_order[j] == choice[j])
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()