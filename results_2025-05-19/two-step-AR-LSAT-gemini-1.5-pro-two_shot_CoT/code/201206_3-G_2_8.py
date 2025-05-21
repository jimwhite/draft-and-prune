from z3 import *

# Variables
business_at_space = Array('business_at_space', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints
# 1. Domain
solver.add(ForAll([i], Implies(And(i >= 1, i <= 7), And(business_at_space[i] >= 0, business_at_space[i] <= 6))))

# 2. Distinctness
solver.add(Distinct([business_at_space[i] for i in range(1, 8)]))

# 3. Pharmacy at End
solver.add(Or(business_at_space[1] == 1, business_at_space[7] == 1))

# 4. Restaurant at Other End
solver.add(Implies(business_at_space[1] == 1, Or(business_at_space[7] == 2, business_at_space[7] == 3)))
solver.add(Implies(business_at_space[7] == 1, Or(business_at_space[1] == 2, business_at_space[1] == 3)))

# 5. Restaurants Separated
solver.add(Sum([If(business_at_space[i] == 2 or business_at_space[i] == 3, 1, 0) for i in range(1,8)]) == 2)
for i in range(1, 7):
    solver.add(Implies(Or(business_at_space[i] == 2, business_at_space[i] == 3), Not(Or(business_at_space[i+1] == 2, business_at_space[i+1] == 3))))
for i in range(1, 6):
    solver.add(Implies(Or(business_at_space[i] == 2, business_at_space[i] == 3), Not(Or(business_at_space[i+2] == 2, business_at_space[i+2] == 3))))


# 6. Pharmacy Next to O or V
solver.add(Implies(business_at_space[1] == 1, Or(business_at_space[2] == 0, business_at_space[2] == 6)))
solver.add(Implies(business_at_space[7] == 1, Or(business_at_space[6] == 0, business_at_space[6] == 6)))

# 7. Toy Store Not Next to V
for i in range(1, 7):
    solver.add(Implies(business_at_space[i] == 5, Not(business_at_space[i+1] == 6)))
for i in range(2, 8):
    solver.add(Implies(business_at_space[i] == 5, Not(business_at_space[i-1] == 6)))


# 8. Veterinarian in Space 5
solver.add(business_at_space[5] == 6)

# Check answer choices
options = [
    business_at_space[2] != 0,  # A
    business_at_space[7] != 1,  # B
    And(business_at_space[4] != 2, business_at_space[4] != 3),  # C
    business_at_space[6] != 4,  # D
    business_at_space[3] != 5   # E
]

for i, option in enumerate(options):
    solver.push()
    solver.add(option)
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
