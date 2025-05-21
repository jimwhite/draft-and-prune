from z3 import *

# Variables
reviews = [[Bool(f'reviews[{i}][{j}]') for j in range(3)] for i in range(5)]
i, j, l, k = Ints('i j l k')

# Solver
solver = Solver()

# Constraints
solver.add([Implies(And(0 <= i, i < 5), Or(reviews[i][0], reviews[i][1], reviews[i][2])) for i in range(5)])
solver.add(Sum([If(reviews[1][k], 1, 0) for k in range(3)]) < Sum([If(reviews[3][k], 1, 0) for k in range(3)]))
solver.add(Sum([If(reviews[2][k], 1, 0) for k in range(3)]) < Sum([If(reviews[3][k], 1, 0) for k in range(3)]))
solver.add([Implies(And(0 <= k, k < 3, reviews[0][k]), Not(reviews[2][k])) for k in range(3)])
solver.add([Implies(And(0 <= k, k < 3, reviews[0][k]), Not(reviews[3][k])) for k in range(3)])
solver.add(reviews[1][1])
solver.add(reviews[4][1])
solver.add(Or([And(0 <= i, i < 5, 0 <= j, j < 5, i != j, And([reviews[i][k] == reviews[j][k] for k in range(3)])) for i in range(5) for j in range(5)]))
solver.add(And([Implies(And(0 <= i, i < 5, 0 <= j, j < 5, 0 <= l, l < 5, i != j, j != l, i != l, And([reviews[i][k] == reviews[j][k] for k in range(3)])), Not(And([reviews[j][k] == reviews[l][k] for k in range(3)]))) for i in range(5) for j in range(5) for l in range(5)]))
solver.add(Sum([If(reviews[i][2], 1, 0) for i in range(5)]) == 3)


# Answer choices
options = [
    Not(reviews[3][2]),  # A
    Not(reviews[4][2]),  # B
    reviews[0][2],      # C
    reviews[2][1],      # D
    reviews[4][0]       # E
]

for i, option in enumerate(options):
    solver.push()
    solver.add(option)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()

