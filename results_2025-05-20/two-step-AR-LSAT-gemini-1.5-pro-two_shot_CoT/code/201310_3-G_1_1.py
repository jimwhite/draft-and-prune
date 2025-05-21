from z3 import *

# Entities (Band IDs)
U = 0
V = 1
W = 2
X = 3
Y = 4
Z = 5

# Variables
band_at_slot = Array('band_at_slot', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints
i = Int('i')
solver.add(ForAll([i], Implies(And(i >= 1, i <= 6), And(band_at_slot[i] >= 0, band_at_slot[i] <= 5))))  # Domain

solver.add(Distinct([band_at_slot[i] for i in range(1, 7)]))  # Distinctness

i = Int('i')
j = Int('j')
solver.add(ForAll([i, j], Implies(And(i >= 1, i <= 6, j >= 1, j <= 6, band_at_slot[i] == V, band_at_slot[j] == Z), i < j)))  # V before Z
solver.add(ForAll([i, j], Implies(And(i >= 1, i <= 6, j >= 1, j <= 6, band_at_slot[i] == W, band_at_slot[j] == X), i < j)))  # W before X
solver.add(ForAll([i, j], Implies(And(i >= 1, i <= 6, j >= 1, j <= 6, band_at_slot[i] == Z, band_at_slot[j] == X), i < j)))  # Z before X

solver.add(Or(band_at_slot[4] == U, band_at_slot[5] == U, band_at_slot[6] == U))  # U in last three
solver.add(Or(band_at_slot[1] == Y, band_at_slot[2] == Y, band_at_slot[3] == Y))  # Y in first three


# Answer choices and their corresponding band IDs
answer_choices = ["Uneasy", "Vegemite", "Wellspring", "Xpert", "Zircon"]
band_ids = [U, V, W, X, Z]

# Check each answer choice
for choice_index, (band_name, band_id) in enumerate(zip(answer_choices, band_ids)):
    solver.push()
    solver.add(band_at_slot[5] == band_id)
    if solver.check() == unsat:
        print(f"Option {chr(65 + choice_index)} is correct")
        exit()
    solver.pop()