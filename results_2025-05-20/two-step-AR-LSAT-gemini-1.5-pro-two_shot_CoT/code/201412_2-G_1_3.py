from z3 import *

# Variables
position = Array('position', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints
i = Int('i')
solver.add(ForAll([i], Implies(And(i >= 0, i <= 5), And(position[i] >= 1, position[i] <= 6))))  # Domain
solver.add(Distinct([position[i] for i in range(6)]))  # Distinctness
solver.add(position[0] != 4)  # Guitarist not 4th
solver.add(position[2] < position[1])  # Percussionist before Keyboard
solver.add(And(position[5] < position[1], position[1] < position[0]))  # Violinist before Keyboard before Guitarist
solver.add(Or(And(position[2] < position[3], Not(position[4] < position[3])), And(Not(position[2] < position[3]), position[4] < position[3])))  # Saxophonist constraint

# Answer choices
choices = [
    position[1] == 1,  # A
    position[0] == 2,  # B
    position[0] < position[3],  # C
    position[0] < position[2],  # D
    position[1] < position[3]   # E
]

for i in range(len(choices)):
    solver.push()
    solver.add(Not(choices[i]))
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()