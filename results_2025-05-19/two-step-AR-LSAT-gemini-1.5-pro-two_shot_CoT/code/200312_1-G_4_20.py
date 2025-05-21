from z3 import *

# Variables
reviews = [[Int(f"reviews[{student}][{play}]") for play in range(3)] for student in range(5)]

# Solver
solver = Solver()

# Constraint 1 (Review Domain)
for student in range(5):
    for play in range(3):
        solver.add(Or(reviews[student][play] == 0, reviews[student][play] == 1))

# Constraint 2 (Each Student Reviews at Least One Play, At Most Three Plays)
for student in range(5):
    solver.add(And(Sum([reviews[student][play] for play in range(3)]) > 0, Sum([reviews[student][play] for play in range(3)]) <= 3))

# Constraint 3 (Three Plays Total)
for play in range(3):
    solver.add(Sum([reviews[student][play] for student in range(5)]) > 0)

# Constraint 4 (Kramer and Lopez Review Fewer than Megregian)
solver.add(Sum([reviews[1][play] for play in range(3)]) < Sum([reviews[3][play] for play in range(3)]))
solver.add(Sum([reviews[2][play] for play in range(3)]) < Sum([reviews[3][play] for play in range(3)]))

# Constraint 5 (Lopez and Megregian disjoint from Jiang)
for play in range(3):
    solver.add(Implies(reviews[0][play] == 1, And(reviews[2][play] == 0, reviews[3][play] == 0)))

# Constraint 6 (Kramer and O'Neill review Tamerlane)
solver.add(reviews[1][1] == 1)
solver.add(reviews[4][1] == 1)

# Constraint 7 (Exactly Two Students Review the Same Plays)
# The error was caused by using `play` as both a bound variable in ForAll and an index in `reviews`.
# We introduce a new bound variable `p` for the ForAll quantifier.
solver.add(Sum([If(ForAll([p], Implies(And(p >= 0, p < 3), reviews[s1][p] == reviews[s2][p])), 1, 0) for s1 in range(5) for s2 in range(s1+1, 5)]) == 1)


# Check answer choices
options = [
    Sum([reviews[0][play] for play in range(3)]) <= Sum([reviews[2][play] for play in range(3)]),  # A
    Sum([reviews[3][play] for play in range(3)]) <= Sum([reviews[0][play] for play in range(3)]),  # B
    Sum([reviews[3][play] for play in range(3)]) <= Sum([reviews[4][play] for play in range(3)]),  # C
    Sum([reviews[4][play] for play in range(3)]) <= Sum([reviews[0][play] for play in range(3)]),  # D
    Sum([reviews[4][play] for play in range(3)]) <= Sum([reviews[1][play] for play in range(3)])   # E
]

for i in range(len(options)):
    solver.push()
    solver.add(Not(options[i]))
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
