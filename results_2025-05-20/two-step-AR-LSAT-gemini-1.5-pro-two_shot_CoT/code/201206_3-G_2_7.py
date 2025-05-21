from z3 import *

# Variables
business_at_space = Array('business_at_space', IntSort(), IntSort())
i = Int('i')
j = Int('j')

# Solver
solver = Solver()

# Constraints
solver.add(ForAll(i, Implies(And(i >= 1, i <= 7), And(business_at_space[i] >= 0, business_at_space[i] <= 6)))) # Domain
solver.add(Distinct([business_at_space[k] for k in range(1, 8)])) # Distinctness
solver.add(Or(business_at_space[1] == 1, business_at_space[7] == 1)) # Pharmacy at end
solver.add(And(Implies(business_at_space[1] == 1, Or(business_at_space[7] == 2, business_at_space[7] == 3)), Implies(business_at_space[7] == 1, Or(business_at_space[1] == 2, business_at_space[1] == 3)))) # Restaurant at other end
solver.add(ForAll([i, j], Implies(And(i >= 1, i <= 7, j >= 1, j <= 7, i != j, Or(business_at_space[i] == 2, business_at_space[i] == 3), Or(business_at_space[j] == 2, business_at_space[j] == 3)), Abs(i - j) >= 3))) # Restaurants separated
solver.add(And(Implies(business_at_space[1] == 1, Or(business_at_space[2] == 0, business_at_space[2] == 6)), Implies(business_at_space[7] == 1, Or(business_at_space[6] == 0, business_at_space[6] == 6)))) # Pharmacy next to O or V
solver.add(And(ForAll(i, Implies(And(i >= 1, i <= 6), Implies(business_at_space[i] == 5, business_at_space[i+1] != 6))), ForAll(i, Implies(And(i >= 2, i <= 7), Implies(business_at_space[i] == 5, business_at_space[i-1] != 6))))) # Toy store not next to V
solver.add(business_at_space[2] == 4) # Shoe store in space 2

# Answer choices
options = [
    business_at_space[5] == 0, # A
    business_at_space[1] == 1, # B
    Or(business_at_space[3] == 2, business_at_space[3] == 3), # C
    business_at_space[6] == 5, # D
    business_at_space[4] == 6  # E
]

for i, option in enumerate(options):
    solver.push()
    solver.add(option)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()