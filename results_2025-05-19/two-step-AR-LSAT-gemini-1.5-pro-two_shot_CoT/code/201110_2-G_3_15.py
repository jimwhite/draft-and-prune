from z3 import *

# Variables
assignment = Function('assignment', IntSort(), IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints
d = Int('d')
r = Int('r')
solver.add(ForAll([d, r], Implies(And(d >= 0, d < 2, r >= 0, r < 4), And(assignment(d, r) >= 0, assignment(d, r) <= 3))))

d = Int('d')
solver.add(ForAll([d], Implies(And(d >= 0, d < 2), Distinct([assignment(d, r) for r in range(4)]))))

b = Int('b')
solver.add(ForAll([b], Implies(And(b >= 0, b <= 3), Distinct([If(assignment(d, r) == b, r + d*4, 10) for d in range(2) for r in range(4)]))))


d = Int('d')
solver.add(ForAll([d], Implies(And(d >= 0, d < 2), assignment(d, 0) != 0)))

d = Int('d')
solver.add(ForAll([d], Implies(And(d >= 0, d < 2), assignment(d, 3) != 3)))

solver.add(Or(assignment(0, 2) == 2, assignment(1, 2) == 2))

solver.add(assignment(0, 3) == assignment(1, 1))

# Check answer choices
choices = [
    (0, 0, 3),  # Reynaldo tests J on the first day
    (1, 0, 3),  # Reynaldo tests J on the second day
    (0, 1, 2),  # Seamus tests H on the first day
    (0, 3, 2),  # Yuki tests H on the first day
    (1, 3, 2)   # Yuki tests H on the second day
]
choice_letters = ['A', 'B', 'C', 'D', 'E']

for i, (day, rider, bike) in enumerate(choices):
    solver.push()
    solver.add(assignment(day, rider) != bike)
    if solver.check() == unsat:
        print(f"Option {choice_letters[i]} is correct")
        exit()
    solver.pop()

