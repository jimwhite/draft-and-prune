from z3 import *

# Variables
auction_day = Array('auction_day', IntSort(), IntSort())
i = Int('i')

# Solver
solver = Solver()

# Constraints
solver.add(ForAll([i], And(auction_day[i] >= 0, auction_day[i] <= 5))) # Constraint 0
solver.add(Distinct([auction_day[i] for i in range(6)])) # Constraint 1
solver.add(auction_day[3] != 0) # Constraint 2
solver.add(Implies(auction_day[0] < auction_day[1], auction_day[2] < auction_day[1])) # Constraint 3
solver.add(auction_day[3] < auction_day[2]) # Constraint 4
solver.add(auction_day[3] < auction_day[5]) # Constraint 5
solver.add(Xor(auction_day[4] < auction_day[0], auction_day[4] < auction_day[5])) # Constraint 6
solver.add(And(auction_day[4] > auction_day[2], auction_day[4] > auction_day[5])) # Constraint 7

# Answer choices
options = [
    auction_day[0] < auction_day[4], # A
    auction_day[4] < auction_day[1], # B
    auction_day[4] < auction_day[3], # C
    auction_day[2] < auction_day[5], # D
    auction_day[3] < auction_day[1]  # E
]

# Check each option
for i in range(len(options)):
    solver.push()
    solver.add(options[i])
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()