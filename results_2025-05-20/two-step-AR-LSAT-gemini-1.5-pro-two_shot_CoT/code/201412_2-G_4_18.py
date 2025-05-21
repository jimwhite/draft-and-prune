from z3 import *

# Variables
assigned = Array('assigned', IntSort(), IntSort())
p = Int('p')

# Solver
solver = Solver()

# Constraints
solver.add(ForAll([p], Implies(And(p >= 0, p < 6), Or(assigned[p] == 0, assigned[p] == 1, assigned[p] == -1)))) # Use And() for combining conditions
solver.add(sum([If(assigned[p] == 0, 1, 0) for p in range(6)]) >= 2)
solver.add(sum([If(assigned[p] == 1, 1, 0) for p in range(6)]) >= 2)
solver.add(Or(And(assigned[0] == 0, assigned[2] == 0), And(assigned[0] == 1, assigned[2] == 1)))
solver.add(Implies(And(assigned[4] != -1, assigned[5] != -1), assigned[4] != assigned[5]))
solver.add(Implies(assigned[1] == 0, assigned[4] == 1))
solver.add(Implies(assigned[3] != 1, And(assigned[2] == 1, assigned[5] == 1)))

# Question Premise
solver.add(Or(And(assigned[2] == 0, assigned[4] == 0), And(assigned[2] == 1, assigned[4] == 1)))

# Answer Choices
negations = [
    assigned[0] != 1,
    assigned[1] != 0,
    assigned[1] != -1,
    assigned[3] != 1,
    assigned[4] != 1
]

for i in range(len(negations)):
    solver.push()
    solver.add(negations[i])
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
