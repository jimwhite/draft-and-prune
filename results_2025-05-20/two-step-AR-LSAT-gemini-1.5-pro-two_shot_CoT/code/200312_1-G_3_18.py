from z3 import *

# Variables
schedule = Array('schedule', IntSort(), IntSort(), IntSort())

# Solver
solver = Solver()

# Constraint 1 (Domain)
c = Int('c')
b = Int('b')
solver.add(ForAll([c, b], Implies(And(c >= 0, c < 3, b >= 0, b < 3), And(schedule[c][b] >= 0, schedule[c][b] < 5))))

# Constraint 2 (No two batches of the same kind on the same day)
c = Int('c')
b1 = Int('b1')
b2 = Int('b2')
solver.add(ForAll([c, b1, b2], Implies(And(c >= 0, c < 3, b1 >= 0, b1 < 3, b2 >= 0, b2 < 3, b1 != b2), schedule[c][b1] != schedule[c][b2])))

# Constraint 3 (At least one batch on Monday)
b = Int('b')
c = Int('c')
solver.add(Or([schedule[c][b] == 0 for c in range(3) for b in range(3)]))

# Constraint 4 (Oatmeal 2nd batch and Peanut Butter 1st batch on same day)
solver.add(schedule[0][1] == schedule[1][0])

# Constraint 5 (Sugar 2nd batch on Thursday)
solver.add(schedule[2][1] == 3)

# Constraint 6 (One kind's 1st batch and another kind's 3rd batch on the same day)
c1 = Int('c1')
c2 = Int('c2')
solver.add(Or([schedule[c1][0] == schedule[c2][2] for c1 in range(3) for c2 in range(3) if c1 != c2]))

# Answer Choices
choices = [
    Not(And([Or([schedule[c][b] == d for c in range(3) for b in range(3)]) for d in range(5)])),
    sum([If(schedule[c][b] == 2, 1, 0) for c in range(3) for b in range(3)]) < 2,
    Not(sum([If(schedule[c][b] == 0, 1, 0) for c in range(3) for b in range(3)]) == 1),
    Not(sum([If(schedule[c][b] == 1, 1, 0) for c in range(3) for b in range(3)]) == 2),
    Not(sum([If(schedule[c][b] == 4, 1, 0) for c in range(3) for b in range(3)]) == 1)
]

for i, choice in enumerate(choices):
    solver.push()
    solver.add(choice)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()

