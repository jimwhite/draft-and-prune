from z3 import *

# Variables
business_at_space = Array('business_at_space', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints
x = Int('x')
i = Int('i')
j = Int('j')

# Constraint 0 (Domain)
solver.add(ForAll([x], Implies(And(x >= 1, x <= 7), And(business_at_space[x] >= 0, business_at_space[x] <= 6))))

# Constraint 1 (Distinctness)
solver.add(Distinct([business_at_space[i] for i in range(1, 8)]))

# Constraint 2 (Pharmacy at end)
solver.add(Or(business_at_space[1] == 1, business_at_space[7] == 1))

# Constraint 3 (Restaurant at other end)
solver.add(Or(And(business_at_space[1] != 1, Or(business_at_space[1] == 2, business_at_space[1] == 3)), And(business_at_space[7] != 1, Or(business_at_space[7] == 2, business_at_space[7] == 3))))

# Constraint 4 (Restaurants separated by 2)
solver.add(ForAll([i, j], Implies(And(i >= 1, i <= 7, j >= 1, j <= 7, i != j, Or(business_at_space[i] == 2, business_at_space[i] == 3), Or(business_at_space[j] == 2, business_at_space[j] == 3)), Abs(i - j) >= 3)))

# Constraint 5 (Pharmacy next to O or V)
solver.add(ForAll([i], Implies(And(i >= 1, i <= 7, business_at_space[i] == 1), Or(And(i > 1, Or(business_at_space[i-1] == 0, business_at_space[i-1] == 6)), And(i < 7, Or(business_at_space[i+1] == 0, business_at_space[i+1] == 6))))))

# Constraint 6 (Toy not next to V)
solver.add(ForAll([i], Implies(And(i >= 1, i <= 7, business_at_space[i] == 5), And(Implies(i > 1, business_at_space[i-1] != 6), Implies(i < 7, business_at_space[i+1] != 6)))))

# Constraint 7 (Shoe store in space 4)
solver.add(business_at_space[4] == 4)

# Answer choices
choices = [
    Exists([i], And(i >= 1, i <= 7, business_at_space[i] == 0, Or(And(i > 1, Or(business_at_space[i-1] == 2, business_at_space[i-1] == 3)), And(i < 7, Or(business_at_space[i+1] == 2, business_at_space[i+1] == 3))))),
    Exists([i], And(i >= 1, i <= 7, business_at_space[i] == 1, Or(And(i > 1, business_at_space[i-1] == 6), And(i < 7, business_at_space[i+1] == 6)))),
    Exists([i], And(i >= 1, i <= 7, business_at_space[i] == 5, Or(And(i > 1, Or(business_at_space[i-1] == 2, business_at_space[i-1] == 3)), And(i < 7, Or(business_at_space[i+1] == 2, business_at_space[i+1] == 3))))),
    Or(business_at_space[3] == 5, business_at_space[5] == 5),
    Or(business_at_space[3] == 6, business_at_space[5] == 6)
]

# Check each answer choice
for i, choice in enumerate(choices):
    solver.push()
    solver.add(Not(choice))
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()