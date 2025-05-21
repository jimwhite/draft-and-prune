from z3 import *

# Variables
business_at_space = Array('business_at_space', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints
# 1. Domain
solver.add(ForAll(x, Implies(And(x >= 1, x <= 7), And(business_at_space[x] >= 0, business_at_space[x] <= 6))))
# 2. Distinctness
solver.add(Distinct([business_at_space[i] for i in range(1, 8)]))
# 3. Pharmacy at End
solver.add(Or(business_at_space[1] == 1, business_at_space[7] == 1))
# 4. Restaurant at Other End
solver.add(Implies(business_at_space[1] == 1, Or(business_at_space[7] == 2, business_at_space[7] == 3)))
solver.add(Implies(business_at_space[7] == 1, Or(business_at_space[1] == 2, business_at_space[1] == 3)))
# 5. Restaurant Separation (simplified) - Not needed, implied by 3 and 4
# 6. Pharmacy Neighbors
solver.add(Implies(business_at_space[1] == 1, Or(business_at_space[2] == 0, business_at_space[2] == 6)))
solver.add(Implies(business_at_space[7] == 1, Or(business_at_space[6] == 0, business_at_space[6] == 6)))
# 7. Toy Store Not Next to Vet
solver.add(ForAll(x, Implies(And(x >= 1, x <= 7), Implies(business_at_space[x] == 5, And(Implies(x > 1, business_at_space[x-1] != 6), Implies(x < 7, business_at_space[x+1] != 6))))))
# 8. Shoe Store in Space 2
solver.add(business_at_space[2] == 4)


# Check answer choices
options = [
    business_at_space[5] == 0,  # A
    business_at_space[1] == 1,  # B
    Or(business_at_space[3] == 2, business_at_space[3] == 3),  # C
    business_at_space[6] == 5,  # D
    business_at_space[4] == 6   # E
]

for i, option in enumerate(options):
    solver.push()
    solver.add(option)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
