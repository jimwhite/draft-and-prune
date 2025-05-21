from z3 import *

# Variables
composition_at_slot = Array('composition_at_slot', IntSort(), IntSort())
i = Int('i')
j = Int('j')

# Solver
solver = Solver()

# Constraints
solver.add(ForAll([i], And(composition_at_slot[i] >= 0, composition_at_slot[i] <= 7)))
solver.add(Distinct([composition_at_slot[i] for i in range(8)]))
solver.add(Or(Exists([i], And(i >= 0, i < 7, composition_at_slot[i] == 7, composition_at_slot[i+1] == 0)), Exists([i], And(i > 0, i <= 7, composition_at_slot[i] == 7, composition_at_slot[i-1] == 5))))
solver.add(Or(Exists([i, j], And(i >= 0, i < 7, j > i + 1, j <= 7, composition_at_slot[i] == 0, composition_at_slot[j] == 5)), Exists([i, j], And(i >= 0, i < 7, j > i + 1, j <= 7, composition_at_slot[i] == 5, composition_at_slot[j] == 0))))
solver.add(Or(composition_at_slot[0] == 3, composition_at_slot[4] == 3))
solver.add(Or(composition_at_slot[7] == 2, composition_at_slot[7] == 1))
solver.add(Exists([i, j], And(i >= 0, i < 7, j > i, j <= 7, composition_at_slot[i] == 4, composition_at_slot[j] == 6)))
solver.add(Or(Exists([i, j], And(i >= 0, i < 7, j > i, j <= 7, composition_at_slot[i] == 3, composition_at_slot[j] == 6)), Exists([i, j], And(i >= 0, i < 7, j > i, j <= 7, composition_at_slot[i] == 6, composition_at_slot[j] == 3))))


# Answer choices
choices = ["second", "third", "fourth", "sixth", "seventh"]
for i, choice in enumerate(choices):
    solver.push()
    solver.add(composition_at_slot[i+1] == 4)
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()