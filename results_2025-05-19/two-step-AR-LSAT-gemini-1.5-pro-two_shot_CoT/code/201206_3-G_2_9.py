from z3 import *

# Variables
business_at_space = Array('business_at_space', IntSort(), IntSort())
O, P, R1, R2, S, T, V = 0, 1, 2, 3, 4, 5, 6

solver = Solver()

# Constraint 1 (Domain)
x = Int('x')
solver.add(ForAll([x], Implies(And(x >= 1, x <= 7), And(business_at_space[x] >= 0, business_at_space[x] <= 6))))

# Constraint 2 (Distinctness)
solver.add(Distinct([business_at_space[i] for i in range(1, 8)]))

# Constraint 3 (Pharmacy at End)
solver.add(Or(business_at_space[1] == P, business_at_space[7] == P))

# Constraint 4 (Restaurant at Other End)
solver.add(Or(business_at_space[1] == R1, business_at_space[1] == R2, business_at_space[7] == R1, business_at_space[7] == R2))

# Constraint 5 (Restaurants Separated)
solver.add(Xor(Or(business_at_space[1] == R1, business_at_space[1] == R2), Or(business_at_space[7] == R1, business_at_space[7] == R2)))
for i in range(1, 6):
    solver.add(Implies(Or(business_at_space[i] == R1, business_at_space[i] == R2), Not(Or(business_at_space[i+1] == R1, business_at_space[i+1] == R2, business_at_space[i+2] == R1, business_at_space[i+2] == R2))))
    solver.add(Implies(Or(business_at_space[i+1] == R1, business_at_space[i+1] == R2), Not(Or(business_at_space[i] == R1, business_at_space[i] == R2, business_at_space[i+2] == R1, business_at_space[i+2] == R2))))
    solver.add(Implies(Or(business_at_space[i+2] == R1, business_at_space[i+2] == R2), Not(Or(business_at_space[i] == R1, business_at_space[i] == R2, business_at_space[i+1] == R1, business_at_space[i+1] == R2))))


# Constraint 6 (Pharmacy Next to O or V)
solver.add(Or(And(business_at_space[1] == P, Or(business_at_space[2] == O, business_at_space[2] == V)), And(business_at_space[7] == P, Or(business_at_space[6] == O, business_at_space[6] == V))))

# Constraint 7 (Toy Store Not Next to V)
for i in range(2, 7):
    solver.add(Implies(business_at_space[i] == T, Not(Or(business_at_space[i+1] == V, business_at_space[i-1] == V))))
solver.add(Implies(business_at_space[1] == T, Not(business_at_space[2] == V)))
solver.add(Implies(business_at_space[7] == T, Not(business_at_space[6] == V)))

# Constraint 8 (Optometrist Next to Shoe Store)
constraints_8 = []
for i in range(1, 7):
    constraints_8.append(Or(And(business_at_space[i] == O, business_at_space[i+1] == S), And(business_at_space[i] == S, business_at_space[i+1] == O)))
solver.add(Or(constraints_8))

options = [
    [P, [R1, R2]],  # Pharmacy and a restaurant
    [P, T],        # Pharmacy and the toy store
    [[R1, R2], [R1, R2]],  # The two restaurants
    [[R1, R2], T],        # A restaurant and the toy store
    [[R1, R2], V]        # A restaurant and the veterinarian
]

for i, option in enumerate(options):
    solver.push()
    constraints_option = []
    for j in range(1, 7):
        constraints_option.append(
            Implies(Or(And(business_at_space[j] == O, business_at_space[j+1] == S),
                       And(business_at_space[j] == S, business_at_space[j+1] == O)),
                   And(Or([business_at_space[j-1] == o for o in ([option[0]] if isinstance(option[0], int) else option[0])]) if j>1 else True,
                       Or([business_at_space[j+2] == o for o in ([option[1]] if isinstance(option[1], int) else option[1])]) if j<6 else True)))
    solver.add(And(constraints_option))

    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
