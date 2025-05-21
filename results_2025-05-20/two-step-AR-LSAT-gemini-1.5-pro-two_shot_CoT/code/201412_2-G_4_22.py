from z3 import *

# Variables
assigned = Array('assigned', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints
p = Int('p')
solver.add(ForAll([p], Implies(And(p >= 0, p < 6), Or(assigned[p] == 0, assigned[p] == 1, assigned[p] == -1))))

u = Int('u')
solver.add(ForAll([u], Implies(And(u >= 0, u < 2), Sum([If(assigned[p] == u, 1, 0) for p in range(6)]) >= 2)))

solver.add(Or(And(assigned[0] == 0, assigned[2] == 0), And(assigned[0] == 1, assigned[2] == 1)))
solver.add(Implies(And(assigned[4] != -1, assigned[5] != -1), assigned[4] != assigned[5]))
solver.add(Implies(assigned[1] == 0, assigned[4] == 1))
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
            solver.add(assigned[j] != 1)
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()