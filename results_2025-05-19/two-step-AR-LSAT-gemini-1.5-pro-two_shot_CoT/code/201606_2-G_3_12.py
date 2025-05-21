from z3 import *

# Entities (as integers)
H = 0
L = 1
M = 2
S = 3
T = 4
V = 5

# Variables
auction_day = Array('auction_day', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints
i = Int('i')
solver.add(ForAll([i], And(auction_day[i] >= 0, auction_day[i] <= 5)))  # Domain
solver.add(Distinct([auction_day[i] for i in range(6)]))  # Distinctness
solver.add(auction_day[S] != 0)  # Sundial not on June 1st
solver.add(Implies(auction_day[H] < auction_day[L], auction_day[M] < auction_day[L]))  # H before L implies M before L
solver.add(auction_day[S] < auction_day[M])  # Sundial before Mirror
solver.add(auction_day[S] < auction_day[V])  # Sundial before Vase
solver.add(Xor(auction_day[T] < auction_day[H], auction_day[T] < auction_day[V]))  # Table before H XOR Table before V

# Answer choices
choices = [
    [H, T, S, L, V, M],
    [L, H, S, M, V, T],
    [H, S, T, M, L, V],
    [S, M, H, T, V, L],
    [V, S, L, H, T, M]
]

# Check each choice
for option_index, choice in enumerate(choices):
    solver.push()
    for day, antique in enumerate(choice):
        solver.add(auction_day[antique] == day)
    if solver.check() == sat:
        print(f"Option {chr(65 + option_index)} is correct")
        exit()
    solver.pop()