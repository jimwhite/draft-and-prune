from z3 import *

# Variables
U, V, W, X, Y, Z = 0, 1, 2, 3, 4, 5
band_at_slot = Array('band_at_slot', IntSort(), IntSort())
i = Int('i')
j = Int('j')

# Solver and base constraints
solver = Solver()
solver.add(ForAll([i], Implies(And(i >= 1, i <= 6), And(band_at_slot[i] >= 0, band_at_slot[i] <= 5))))
solver.add(Distinct([band_at_slot[i] for i in range(1, 7)]))
solver.add(ForAll([i, j], Implies(And(i >= 1, i <= 6, j >= 1, j <= 6, band_at_slot[i] == V, band_at_slot[j] == Z), i < j)))
solver.add(ForAll([i, j], Implies(And(i >= 1, i <= 6, j >= 1, j <= 6, band_at_slot[i] == W, band_at_slot[j] == X), i < j)))
solver.add(ForAll([i, j], Implies(And(i >= 1, i <= 6, j >= 1, j <= 6, band_at_slot[i] == Z, band_at_slot[j] == X), i < j)))
solver.add(Or(band_at_slot[4] == U, band_at_slot[5] == U, band_at_slot[6] == U))
solver.add(Or(band_at_slot[1] == Y, band_at_slot[2] == Y, band_at_slot[3] == Y))


# Check answer choices
possible_bands = []
for b, band_name in [(V, "Vegemite"), (W, "Wellspring"), (Y, "Yardsign"), (Z, "Zircon")]:
    solver.push()
    solver.add(band_at_slot[1] == b)
    if solver.check() == sat:
        possible_bands.append(band_name)
    solver.pop()

options = [
    ["Yardsign"],
    ["Vegemite", "Wellspring"],
    ["Vegemite", "Yardsign"],
    ["Vegemite", "Wellspring", "Yardsign"],
    ["Vegemite", "Wellspring", "Yardsign", "Zircon"]
]

for i, option in enumerate(options):
    if set(option) == set(possible_bands):
        print(f"Option {chr(65 + i)} is correct")
        exit()