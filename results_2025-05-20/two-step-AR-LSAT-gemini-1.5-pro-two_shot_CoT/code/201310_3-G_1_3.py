from z3 import *

# Entities (as integers)
U = 0
V = 1
W = 2
X = 3
Y = 4
Z = 5

# Variables
band_at_slot = Array('band_at_slot', IntSort(), IntSort())
i, j, k = Ints('i j k')

# Solver
solver = Solver()

# Constraints
solver.add(ForAll([i], Implies(And(i >= 1, i <= 6), And(band_at_slot[i] >= 0, band_at_slot[i] <= 5))))  # Domain
solver.add(Distinct([band_at_slot[i] for i in range(1, 7)]))  # Distinctness
solver.add(ForAll([i, j], Implies(And(i >= 1, i <= 6, j >= 1, j <= 6, band_at_slot[i] == V, band_at_slot[j] == Z), i < j)))  # V before Z
solver.add(ForAll([i, j, k], Implies(And(i >= 1, i <= 6, j >= 1, j <= 6, k >= 1, k <= 6, band_at_slot[i] == W, band_at_slot[j] == Z, band_at_slot[k] == X), And(i < k, j < k))))  # W and Z before X
solver.add(ForAll([i], Implies(And(i >= 1, i <= 6, band_at_slot[i] == U), Or(i == 4, i == 5, i == 6))))  # U in last three
solver.add(ForAll([i], Implies(And(i >= 1, i <= 6, band_at_slot[i] == Y), Or(i == 1, i == 2, i == 3))))  # Y in first three
solver.add(band_at_slot[3] == V)  # V in slot 3


# Answer choices and their negations
options = [
    (U, X, "A"),  # U before X
    (W, Z, "B"),  # W before Z
    (X, U, "C"),  # X before U
    (Y, W, "D"),  # Y before W
    (Z, U, "E")   # Z before U
]

for band1, band2, option_letter in options:
    solver.push()
    solver.add(Exists([i, j], And(i >= 1, i <= 6, j >= 1, j <= 6, band_at_slot[i] == band1, band_at_slot[j] == band2, i > j))) # Negation
    if solver.check() == unsat:
        print(f"Option {option_letter} is correct")
        exit()
    solver.pop()