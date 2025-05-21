from z3 import *

# Variables
book_shelf = Array('book_shelf', IntSort(), IntSort())
b = Int('b')
s = Int('s')

# Solver
solver = Solver()

# Constraints
solver.add(ForAll([b], And(book_shelf[b] >= 0, book_shelf[b] <= 2)))  # Domain
solver.add(ForAll([s], Sum([If(book_shelf[b] == s, 1, 0) for b in range(8)]) >= 2))  # At least two on each shelf
solver.add(Sum([If(book_shelf[b] == 2, 1, 0) for b in range(8)]) > Sum([If(book_shelf[b] == 0, 1, 0) for b in range(8)]))  # More on bottom than top
solver.add(book_shelf[3] == 1)  # I on middle
solver.add(book_shelf[4] < book_shelf[0])  # K higher than F
solver.add(book_shelf[7] < book_shelf[5])  # O higher than L
solver.add(book_shelf[0] == book_shelf[6])  # F and M same shelf
solver.add(book_shelf[5] < book_shelf[2])  # L higher than H

# Answer choices
options = [
    (book_shelf[0] != book_shelf[1]),  # F != G
    (book_shelf[1] != book_shelf[2]),  # G != H
    (book_shelf[2] != book_shelf[6]),  # H != M
    (book_shelf[3] != book_shelf[1]),  # I != G
    (book_shelf[4] != book_shelf[7])   # K != O
]

for i, option in enumerate(options):
    solver.push()
    solver.add(option)
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()