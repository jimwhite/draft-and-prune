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

# Create a solver
solver = Solver()

# Constraint 0 (Domain)
i = Int('i')
solver.add(ForAll([i], Implies(And(i >= 0, i < 6), And(auction_day[i] >= 0, auction_day[i] < 6))))

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
choices = [
    (M, 1, 'A'),  # Mirror on June 2nd
    (L, 1, 'B'),  # Lamp on June 2nd
    (V, 1, 'C'),  # Vase on June 2nd
    (L, 2, 'D'),  # Lamp on June 3rd
    (M, 4, 'E')   # Mirror on June 5th
]

for antique, day, option in choices:
    solver.push()
    solver.add(auction_day[antique] == day)
    if solver.check() == sat:
        print(f"Option {option} is correct")
        exit()
    solver.pop()