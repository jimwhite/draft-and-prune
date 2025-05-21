from z3 import *

# Define variables
auction_day = Array('auction_day', IntSort(), IntSort())
solver = Solver()

# Define antique IDs
H = 0
L = 1
M = 2
S = 3
T = 4
V = 5

# Constraint 0: Domain
i = Int('i')
solver.add(ForAll([i], Implies(And(i >= 0, i < 6), And(auction_day[i] >= 1, auction_day[i] <= 6))))

# Constraint 1: Distinctness
solver.add(Distinct([auction_day[i] for i in range(6)]))

# Constraint 2: Sundial not on June 1st
solver.add(auction_day[S] != 1)

# Constraint 3: Harmonica before Lamp implies Mirror before Lamp
solver.add(Implies(auction_day[H] < auction_day[L], auction_day[M] < auction_day[L]))

# Constraint 4: Sundial before Mirror
solver.add(auction_day[S] < auction_day[M])

# Constraint 5: Sundial before Vase
solver.add(auction_day[S] < auction_day[V])

# Constraint 6: Table before Harmonica XOR Table before Vase
solver.add(Xor(auction_day[T] < auction_day[H], auction_day[T] < auction_day[V]))

# Check answer choices
options = [
    (S, 5),  # A
    (S, 4),  # B
    (L, 5, M, 6),  # C
    (T, 3, L, 4),  # D
    (H, 2, V, 3)   # E
]

for option_index, option in enumerate(options):
    solver.push()
    if len(option) == 2:
        solver.add(auction_day[option[0]] == option[1])
    else:
        solver.add(And(auction_day[option[0]] == option[1], auction_day[option[2]] == option[3]))
    if solver.check() == sat:
        print(f"Option {chr(65 + option_index)} is correct")
        exit()
    solver.pop()