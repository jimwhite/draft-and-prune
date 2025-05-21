from z3 import *

# Define variables
assigned = Array('assigned', IntSort(), IntSort())
p = Int('p')

# Create solver and add constraints
solver = Solver()

# Constraint 1: Domain
solver.add(ForAll([p], And(assigned[p] >= 0, assigned[p] <= 2)))

# Constraint 2: At least two at each university
count_silva = Sum([If(assigned[p] == 0, 1, 0) for p in range(6)])
count_thorne = Sum([If(assigned[p] == 1, 1, 0) for p in range(6)])
solver.add(And(count_silva >= 2, count_thorne >= 2))

# Constraint 3: No photographer at both
solver.add(ForAll([p], Implies(assigned[p] != 2, Or(assigned[p] == 0, assigned[p] == 1))))
solver.add(ForAll([p], Implies(Or(assigned[p] == 0, assigned[p] == 1), assigned[p] != 2)))


# Constraint 4: Frost and Heideck together
solver.add(assigned[0] == assigned[2])
solver.add(assigned[0] != 2)

# Constraint 5: Lai and Mays different
solver.add(Implies(And(assigned[4] != 2, assigned[5] != 2), assigned[4] != assigned[5]))

# Constraint 6: Gonzalez at Silva implies Lai at Thorne
solver.add(Implies(assigned[1] == 0, assigned[4] == 1))

# Constraint 7: Knutson not at Thorne implies Heideck and Mays at Thorne
solver.add(Implies(assigned[3] != 1, And(assigned[2] == 1, assigned[5] == 1)))

# Answer choices
choices = [
    [0, 1, 2, 5],
    [0, 2, 3, 5],
    [1, 3, 4],
    [1, 3, 5],
    [3, 5]
]

for i, choice in enumerate(choices):
    solver.push()
    for j in range(6):
        if j in choice:
            solver.add(assigned[j] == 1)
        else:
            solver.add(Or(assigned[j] == 0, assigned[j] == 2))

    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()