from z3 import *

# Variables
book_shelf = Array('book_shelf', IntSort(), IntSort())
s = Int('s')
b = Int('b')

# Solver
solver = Solver()

# Constraints
solver.add(ForAll([b], And(book_shelf[b] >= 0, book_shelf[b] <= 2)))
solver.add(ForAll([s], Implies(And(s >= 0, s <= 2), Sum([If(book_shelf[i] == s, 1, 0) for i in range(8)]) >= 2)))
solver.add(Sum([If(book_shelf[i] == 2, 1, 0) for i in range(8)]) > Sum([If(book_shelf[i] == 0, 1, 0) for i in range(8)]))
solver.add(book_shelf[3] == 1)
solver.add(book_shelf[4] < book_shelf[0])
solver.add(book_shelf[7] < book_shelf[5])
solver.add(book_shelf[0] == book_shelf[6])

# Answer choices
options = [
    [0, 6],
    [0, 2, 6],
    [1, 2, 4],
    [0, 1, 6, 7],
    [1, 2, 5, 6]
]

for option_index, option in enumerate(options):
    solver.push()
    for book_on_shelf in option:
        solver.add(book_shelf[book_on_shelf] == 2)
    for book_not_on_shelf in range(8):
        if book_not_on_shelf not in option:
            solver.add(book_shelf[book_not_on_shelf] != 2) # Corrected constraint

    if solver.check() == sat:
        print(f"Option {chr(65 + option_index)} is correct")
        exit()
    solver.pop()
