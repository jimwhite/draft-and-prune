from z3 import *

# Constants for antiques and days
H, L, M, S, T, V = 0, 1, 2, 3, 4, 5

# Variables
auction_day = Array('auction_day', IntSort(), IntSort())
i = Int('i')

# Solver
solver = Solver()

# Constraints
solver.add(ForAll([i], And(auction_day[i] >= 0, auction_day[i] <= 5)))
solver.add(Distinct([auction_day[i] for i in range(6)]))
solver.add(auction_day[S] != 0)
solver.add(Implies(auction_day[H] < auction_day[L], auction_day[M] < auction_day[L]))
solver.add(auction_day[S] < auction_day[M])
solver.add(auction_day[S] < auction_day[V])
solver.add(Xor(auction_day[T] < auction_day[H], auction_day[T] < auction_day[V]))

# Answer choices
choices = [
    ([T, 1], [L, 2]),  # A
    ([S, 1], [V, 2]),  # B
    ([M, 2], [S, 3]),  # C  <-- Incorrect order S < M
    ([V, 3], [S, 4]),  # D  <-- Incorrect order S < V
    ([S, 3], [T, 4])   # E
]

# Check each choice
for option, choice in enumerate(choices, ord('A')):
    solver.push()
    solver.add(auction_day[choice[0][0]] == choice[0][1])
    solver.add(auction_day[choice[1][0]] == choice[1][1])
    if solver.check() == sat:
        print(f"Option {chr(option)} is correct")
        exit()
    solver.pop()
