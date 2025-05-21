from z3 import *

# Variables
auction_day = Array('auction_day', IntSort(), IntSort())
i = Int('i')

# Solver
solver = Solver()

# Constraints
solver.add(ForAll([i], And(auction_day[i] >= 0, auction_day[i] <= 5)))
solver.add(Distinct([auction_day[i] for i in range(6)]))
solver.add(auction_day[3] != 0)
solver.add(Implies(auction_day[0] < auction_day[1], auction_day[2] < auction_day[1]))
solver.add(auction_day[3] < auction_day[2])
solver.add(auction_day[3] < auction_day[5])
solver.add(Xor(auction_day[4] < auction_day[0], auction_day[4] < auction_day[5]))

# Answer choices
options = [
    (2, 1),  # A: Mirror on June 2nd
    (1, 1),  # B: Lamp on June 2nd
    (5, 1),  # C: Vase on June 2nd
    (1, 2),  # D: Lamp on June 3rd
    (2, 4)   # E: Mirror on June 5th
]

for option_index, (item, day) in enumerate(options):
    solver.push()
    solver.add(auction_day[item] == day)
    if solver.check() == sat:
        print(f"Option {chr(65 + option_index)} is correct")
        exit()
    solver.pop()