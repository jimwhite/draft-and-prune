from z3 import *

# Variables
book_shelf = Array('book_shelf', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints
b = Int('b')
solver.add(ForAll([b], And(book_shelf[b] >= 0, book_shelf[b] <= 2)))

top_count = Sum([If(book_shelf[i] == 0, 1, 0) for i in range(8)])
middle_count = Sum([If(book_shelf[i] == 1, 1, 0) for i in range(8)])
bottom_count = Sum([If(book_shelf[i] == 2, 1, 0) for i in range(8)])

solver.add(top_count + middle_count + bottom_count == 8)
solver.add(And(top_count >= 2, middle_count >= 2, bottom_count >= 2))
solver.add(bottom_count > top_count)
solver.add(book_shelf[3] == 1)
solver.add(book_shelf[4] < book_shelf[0])
solver.add(book_shelf[7] < book_shelf[5])
solver.add(book_shelf[0] == book_shelf[6])

# Check answer choices
negations = [
    book_shelf[7] >= book_shelf[6],
    book_shelf[4] >= book_shelf[1],
    book_shelf[3] >= book_shelf[0],
    book_shelf[1] >= book_shelf[7],
    book_shelf[0] >= book_shelf[5]
]

for i, negation in enumerate(negations):
    solver.push()
    solver.add(negation)
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()