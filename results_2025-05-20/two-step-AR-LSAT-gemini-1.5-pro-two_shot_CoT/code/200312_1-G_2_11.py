from z3 import *

# Variables
bay_F = Int('bay_F')
bay_G = Int('bay_G')
bay_L = Int('bay_L')
bay_M = Int('bay_M')
bay_P = Int('bay_P')
bay_T = Int('bay_T')

solver = Solver()

# Constraint 0 (Domain)
solver.add(And(bay_F >= 1, bay_F <= 6, bay_G >= 1, bay_G <= 6, bay_L >= 1, bay_L <= 6, bay_M >= 1, bay_M <= 6, bay_P >= 1, bay_P <= 6, bay_T >= 1, bay_T <= 6))

# Constraint 1 (Distinctness)
solver.add(Distinct(bay_F, bay_G, bay_L, bay_M, bay_P, bay_T))

# Constraint 2 (Grain > Livestock)
solver.add(bay_G > bay_L)

# Constraint 3 (Livestock > Textiles)
solver.add(bay_L > bay_T)

# Constraint 4 (Produce > Fuel)
solver.add(bay_P > bay_F)

# Constraint 5 (Textiles next to Produce)
solver.add(Abs(bay_T - bay_P) == 1)

# Constraint 6 (Produce next to Livestock)
solver.add(Abs(bay_P - bay_L) == 1)

# Answer choices
choices = [
    (bay_F == 2, 'A'),
    (bay_P == 4, 'B'),
    (bay_T == 4, 'C'),
    (bay_G == 5, 'D'),
    (bay_M == 5, 'E')
]

for choice, option in choices:
    solver.push()
    solver.add(choice)
    if solver.check() == unsat:
        print(f"Option {option} is correct")
        exit()
    solver.pop()