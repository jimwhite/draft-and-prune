from z3 import *

# Variables
book_shelf = Array('book_shelf', IntSort(), IntSort())
b = Int('b')
s = Int('s')

# Solver
solver = Solver()

# Constraints
solver.add(ForAll([b], Implies(And(b >= 0, b < 8), And(book_shelf[b] >= 0, book_shelf[b] <= 2)))) # Fixed: Added range check for b
solver.add(ForAll([s], Implies(And(s >= 0, s <= 2), Sum([If(book_shelf[i] == s, 1, 0) for i in range(8)]) >= 2)))
solver.add(Sum([If(book_shelf[i] == 2, 1, 0) for i in range(8)]) > Sum([If(book_shelf[i] == 0, 1, 0) for i in range(8)]))
solver.add(book_shelf[3] == 1)
solver.add(book_shelf[4] < book_shelf[0])
solver.add(book_shelf[7] < book_shelf[5])
solver.add(book_shelf[0] == book_shelf[6])
solver.add(book_shelf[1] == 0)

# Answer choices
options = [
    [2, 3],  # H, I
    [3, 5],  # I, L
    [2, 3, 5],  # H, I, L
    [3, 4, 5],  # I, K, L
    [0, 3, 6]   # F, I, M
]

for i, option in enumerate(options):
    solver.push()
    for book in option:
        solver.add(book_shelf[book] == 1)
    other_books = [j for j in range(8) if j not in option]
    for book in other_books:
        solver.add(book_shelf[book] != 1)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()

