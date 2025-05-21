from z3 import *

# Define constants for antiques
H = 0
L = 1
M = 2
S = 3
T = 4
V = 5

# Define the solver
solver = Solver()

# Define the auction schedule array
auction_schedule = Array('auction_schedule', IntSort(), IntSort())

# Define day variables for each antique
day_H, day_L, day_M, day_S, day_T, day_V = Ints('day_H day_L day_M day_S day_T day_V')

# Constraint 0: Domain for array values
d = Int('d')
solver.add(ForAll([d], Implies(And(d >= 0, d < 6), And(auction_schedule[d] >= 0, auction_schedule[d] <= 5))))

# Constraint 1: Distinct values in array
solver.add(Distinct([auction_schedule[d] for d in range(6)]))

# Constraint 2: Domain for day variables
solver.add(And(0 <= day_H, day_H < 6, 0 <= day_L, day_L < 6, 0 <= day_M, day_M < 6, 0 <= day_S, day_S < 6, 0 <= day_T, day_T < 6, 0 <= day_V, day_V < 6))

# Constraint 3: Distinct days for each antique
solver.add(Distinct(day_H, day_L, day_M, day_S, day_T, day_V))

# Constraint 4: Link array and day variables
solver.add(And(auction_schedule[day_H] == H, auction_schedule[day_L] == L, auction_schedule[day_M] == M, auction_schedule[day_S] == S, auction_schedule[day_T] == T, auction_schedule[day_V] == V))

# Constraint 5: Sundial not on June 1st
solver.add(day_S != 0)

# Constraint 6: Harmonica before Lamp implies Mirror before Lamp
solver.add(Implies(day_H < day_L, day_M < day_L))

# Constraint 7: Sundial before Mirror
solver.add(day_S < day_M)

# Constraint 8: Sundial before Vase
solver.add(day_S < day_V)

# Constraint 9: Table before Harmonica XOR Table before Vase
solver.add(Xor(day_T < day_H, day_T < day_V))

# Answer choices
choices = [
    [H, T, S, L, V, M],
    [L, H, S, M, V, T],
    [H, S, T, M, L, V],
    [S, M, H, T, V, L],
    [V, S, L, H, T, M]
]

# Check each answer choice
for i, choice in enumerate(choices):
    solver.push()
    for day, antique in enumerate(choice):
        solver.add(auction_schedule[day] == antique)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()