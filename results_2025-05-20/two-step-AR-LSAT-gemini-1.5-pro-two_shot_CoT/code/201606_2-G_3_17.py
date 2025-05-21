from z3 import *

# Define constants for antiques and days
H = 0
L = 1
M = 2
S = 3
T = 4
V = 5

# Define the variable
auction_day = Array('auction_day', IntSort(), IntSort())

# Create the solver and add constraints
solver = Solver()

# Constraint 0 (Domain)
solver.add(And([And(auction_day[i] >= 0, auction_day[i] <= 5) for i in range(6)]))

# Constraint 1 (Distinctness)
solver.add(Distinct([auction_day[i] for i in range(6)]))

# Constraint 2 (Sundial not on June 1st)
solver.add(auction_day[S] != 0)

# Constraint 3 (Harmonica before Lamp implies Mirror before Lamp)
solver.add(Implies(auction_day[H] < auction_day[L], auction_day[M] < auction_day[L]))

# Constraint 4 (Sundial before Mirror)
solver.add(auction_day[S] < auction_day[M])

# Constraint 5 (Sundial before Vase)
solver.add(auction_day[S] < auction_day[V])

# Constraint 6 (Table before Harmonica XOR Table before Vase)
solver.add(Xor(auction_day[T] < auction_day[H], auction_day[T] < auction_day[V]))

# Check answer choices
options = [
    (S, 4),  # A: Sundial on June 5th
    (S, 3),  # B: Sundial on June 4th
    (L, 4, M, 5),  # C: Lamp on June 5th and Mirror on June 6th
    (T, 2, L, 3),  # D: Table on June 3rd and Lamp on June 4th
    (H, 1, V, 2)   # E: Harmonica on June 2nd and Vase on June 3rd
]

for i, option in enumerate(options):
    solver.push()
    if len(option) == 2:
        solver.add(auction_day[option[0]] == option[1])
    else:
        solver.add(And(auction_day[option[0]] == option[1], auction_day[option[2]] == option[3]))
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()