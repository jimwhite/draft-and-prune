from z3 import *

# Variables
pos = Array('pos', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraint 0: Domain and Range
for i in range(8):
    solver.add(And(pos[i] >= 0, pos[i] < 8))

# Constraint 1: Permutation
solver.add(Distinct([pos[i] for i in range(8)]))

# Constraint 2: T before F or after R
solver.add(Or(pos[7] + 1 == pos[0], pos[5] + 1 == pos[7]))

# Constraint 3: Two between F and R
solver.add(Or(pos[5] - pos[0] >= 3, pos[0] - pos[5] >= 3))

# Constraint 4: O is first or fifth
solver.add(Or(pos[3] == 0, pos[3] == 4))

# Constraint 5: Eighth is L or H
solver.add(Or(pos[2] == 7, pos[1] == 7))

# Constraint 6: P before S
solver.add(pos[4] < pos[6])

# Constraint 7: One between O and S
solver.add(Or(pos[6] - pos[3] >= 2, pos[3] - pos[6] >= 2))

# Constraint 8: Two after F before O
solver.add(pos[3] == pos[0] + 3)

# Answer choices
answers = [0, 2, 3, 5, 6]
answer_options = ['A', 'B', 'C', 'D', 'E']

for i, answer in enumerate(answers):
    solver.push()
    solver.add(Not(pos[5] == answer))
    if solver.check() == unsat:
        print(f"Option {answer_options[i]} is correct")
        exit()
    solver.pop()