from z3 import *

# Define constants for antiques
H = 0
L = 1
M = 2
S = 3
T = 4
V = 5

# Define the variable
auction_day = Array('auction_day', IntSort(), IntSort())
solver = Solver()
i = Int('i')

# Add constraints
solver.add(ForAll([i], And(auction_day[i] >= 0, auction_day[i] <= 5)))
solver.add(Distinct([auction_day[i] for i in range(6)]))
solver.add(auction_day[S] != 0)
solver.add(Implies(auction_day[H] < auction_day[L], auction_day[M] < auction_day[L]))
solver.add(auction_day[S] < auction_day[M])
solver.add(auction_day[S] < auction_day[V])
solver.add(Xor(auction_day[T] < auction_day[H], auction_day[T] < auction_day[V]))

# Check answer choices
choices = [
    ([T, 1], [L, 2]),  # A
    ([S, 1], [V, 2]),  # B
    ([M, 2], [S, 3]),  # C
    ([V, 3], [S, 4]),  # D
    ([S, 3], [T, 4])   # E
]

for option, (choice1, choice2) in enumerate(choices):
    solver.push()
    solver.add(auction_day[choice1[0]] == choice1[1])
    solver.add(auction_day[choice2[0]] == choice2[1])
    if solver.check() == sat:
        print(f"Option {chr(65 + option)} is correct")
        exit()
    solver.pop()