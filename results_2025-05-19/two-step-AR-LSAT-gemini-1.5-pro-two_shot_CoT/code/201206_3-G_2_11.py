from z3 import *

# Variables
business_at_space = Array('business_at_space', IntSort(), IntSort())
x = Int('x')
i = Int('i')

# Solver
solver = Solver()

# Constraints 0 (Domain)
solver.add(ForAll([x], Implies(And(x >= 1, x <= 7), And(business_at_space[x] >= 0, business_at_space[x] <= 6))))

# Constraint 1 (Distinctness)
solver.add(Distinct([business_at_space[i] for i in range(1, 8)]))

# Constraint 2 (Pharmacy at end)
solver.add(Or(business_at_space[1] == 1, business_at_space[7] == 1))

# Constraint 3 (Restaurant at other end)
solver.add(Or(business_at_space[1] == 2, business_at_space[1] == 3, business_at_space[7] == 2, business_at_space[7] == 3))

# Constraint 5 (Pharmacy next to Optometrist or Veterinarian)
solver.add(Implies(business_at_space[1] == 1, Or(business_at_space[2] == 0, business_at_space[2] == 6)))
solver.add(Implies(business_at_space[7] == 1, Or(business_at_space[6] == 0, business_at_space[6] == 6)))

# Constraint 6 (Toy store not next to Veterinarian)
for i in range(1, 7):
    solver.add(Implies(business_at_space[i] == 5, business_at_space[i+1] != 6))
    solver.add(Implies(business_at_space[i] == 6, business_at_space[i+1] != 5))


# Constraint 4 (Restaurants separated by at least two)
for i in range(1, 6):
    solver.add(Implies(Or(business_at_space[i] == 2, business_at_space[i] == 3), Not(Or(business_at_space[i+1] == 2, business_at_space[i+1] == 3, business_at_space[i+2] == 2, business_at_space[i+2] == 3))))
if solver.check() == sat:
    m = solver.model()
    original_count = len(set(m[business_at_space[i]].as_long() for i in range(1, 8))) # Count distinct assigned values

else:
    original_count = 0



options = [
    # A: A restaurant must be in either space 3, 4, or 5.
    Or(business_at_space[3] == 2, business_at_space[3] == 3, business_at_space[4] == 2, business_at_space[4] == 3, business_at_space[5] == 2, business_at_space[5] == 3),
    # B: A restaurant must be next to either the optometrist or the veterinarian.
    Or(And([Implies(business_at_space[i] == 0, Or(business_at_space[i+1] == 2, business_at_space[i+1] == 3, business_at_space[i-1] == 2, business_at_space[i-1] == 3)) for i in range(2,7)]), And([Implies(business_at_space[i] == 6, Or(business_at_space[i+1] == 2, business_at_space[i+1] == 3, business_at_space[i-1] == 2, business_at_space[i-1] == 3)) for i in range(2,7)])),
    # C: Either the toy store or the veterinarian must be somewhere between the two restaurants.

    # D: No more than two businesses can separate the pharmacy and the restaurant nearest it. 
    Or(Implies(business_at_space[1] == 1, Or(business_at_space[2] == 2, business_at_space[2] == 3, business_at_space[3] == 2, business_at_space[3] == 3, business_at_space[4] == 2, business_at_space[4] == 3)),
    Implies(business_at_space[7] == 1, Or(business_at_space[4] == 2, business_at_space[4] == 3, business_at_space[5] == 2, business_at_space[5] == 3, business_at_space[6] == 2, business_at_space[6] == 3))),
    # E: The optometrist cannot be next to the shoe store.
    And([Implies(business_at_space[i] == 0, business_at_space[i+1] != 4) for i in range(1,7)] + [Implies(business_at_space[i] == 4, business_at_space[i+1] != 0) for i in range(1,7)])
]

for idx, option in enumerate(options):
    solver.push()
    solver.add(option)
    if solver.check() == sat:
        m = solver.model()
        current_count = len(set(m[business_at_space[i]].as_long() for i in range(1, 8))) # Count distinct assigned values
    else:
        current_count = 0
    solver.pop()
    if original_count == current_count and original_count != 0:
        print(f"Option {chr(65 + idx)} is correct")
        exit()

