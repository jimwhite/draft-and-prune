from z3 import *

# Define variables
I = 0
S = 1
T = 2
W = 0
V = 1

target = [[Int("target_%s_%s" % (c, r)) for r in range(2)] for c in range(3)]

solver = Solver()

# C1: All targets are 1, 2, or 3 days
for c in range(3):
    for r in range(2):
        solver.add(And(target[c][r] >= 1, target[c][r] <= 3))

# C2: Website target ≤ Voicemail target
solver.add(target[I][W] <= target[I][V])
solver.add(target[S][W] <= target[S][V])
solver.add(target[T][W] <= target[T][V])

# C3: Image's voicemail target < other voicemail targets
solver.add(target[I][V] < target[S][V])
solver.add(target[I][V] < target[T][V])

# C4: Solide's website target < Truvest's website target
solver.add(target[S][W] < target[T][W])

options = [
    (1, W),  # 1-day website target
    (2, V),  # 2-day voicemail target
    (2, W),  # 2-day website target
    (3, V),  # 3-day voicemail target
    (3, W),  # 3-day website target
]

for option_index, (days, request_type) in enumerate(options):
    solver.push()
    solver.add(Or(
        And(target[I][request_type] == days, target[S][request_type] == days),
        And(target[I][request_type] == days, target[T][request_type] == days),
        And(target[S][request_type] == days, target[T][request_type] == days)
    ))
    if solver.check() == unsat:
        print(f"Option {chr(65 + option_index)} is correct")
        exit()
    solver.pop()