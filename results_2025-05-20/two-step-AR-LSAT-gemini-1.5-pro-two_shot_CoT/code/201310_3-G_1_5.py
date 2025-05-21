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
i = Int('i')
j = Int('j')

# Solver
solver = Solver()

# Constraints
solver.add(ForAll([i], And(i >= 0, i < 6, band_at_slot[i] >= 0, band_at_slot[i] < 6))) # Domain
solver.add(Distinct([band_at_slot[k] for k in range(6)])) # Distinctness
solver.add(Exists([i, j], And(i >= 0, i < 6, j >= 0, j < 6, i < j, band_at_slot[i] == V, band_at_slot[j] == Z))) # V before Z
solver.add(Exists([i, j], And(i >= 0, i < 6, j >= 0, j < 6, i < j, band_at_slot[i] == W, band_at_slot[j] == X))) # W before X
solver.add(Exists([i, j], And(i >= 0, i < 6, j >= 0, j < 6, i < j, band_at_slot[i] == Z, band_at_slot[j] == X))) # Z before X
solver.add(Or(band_at_slot[3] == U, band_at_slot[4] == U, band_at_slot[5] == U)) # U in last three
solver.add(Or(band_at_slot[0] == Y, band_at_slot[1] == Y, band_at_slot[2] == Y)) # Y in first three


# Answer Choices
options = [
    ["Yardsign"],
    ["Vegemite", "Wellspring"],
    ["Vegemite", "Yardsign"],
    ["Vegemite", "Wellspring", "Yardsign"],
    ["Vegemite", "Wellspring", "Yardsign", "Zircon"]
]

band_names = ["Uneasy", "Vegemite", "Wellspring", "Xpert", "Yardsign", "Zircon"]

# Check each option
for option_index, option in enumerate(options):
    solver.push()
    possible_bands_slot1 = []
    for band_id in range(6):
        solver.push()
        solver.add(band_at_slot[0] == band_id)
        if solver.check() == sat:
            possible_bands_slot1.append(band_names[band_id])
        solver.pop()

    option_band_names = option
    if set(possible_bands_slot1) == set(option_band_names):
        print(f"Option {chr(65 + option_index)} is correct")
        exit()
    solver.pop()