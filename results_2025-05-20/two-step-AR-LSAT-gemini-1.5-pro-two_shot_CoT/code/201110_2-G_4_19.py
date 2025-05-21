from z3 import *

# Variables
book_shelf = Array('book_shelf', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints
b = Int('b')
s = Int('s')

# Constraint 1: Domain
solver.add(ForAll([b], Implies(And(b >= 0, b < 8), And(book_shelf[b] >= 0, book_shelf[b] <= 2))))

# Constraint 2: At least two on each shelf
solver.add(ForAll([s], Implies(And(s >= 0, s <= 2), Sum([If(book_shelf[b] == s, 1, 0) for b in range(8)]) >= 2)))

# Constraint 3: More on bottom than top
solver.add(Sum([If(book_shelf[b] == 2, 1, 0) for b in range(8)]) > Sum([If(book_shelf[b] == 0, 1, 0) for b in range(8)]))

# Constraint 4: I on middle
solver.add(book_shelf[3] == 1)

# Constraint 5: K higher than F
solver.add(book_shelf[4] < book_shelf[0])

# Constraint 6: O higher than L
solver.add(book_shelf[7] < book_shelf[5])

# Constraint 7: F and M on same shelf
solver.add(book_shelf[0] == book_shelf[6])

# Answer choices
choices = ["F, M", "F, H, M", "G, H, K", "F, G, M, O", "G, H, L, M"]
book_map = {'F': 0, 'G': 1, 'H': 2, 'I': 3, 'K': 4, 'L': 5, 'M': 6, 'O': 7}

for i, choice in enumerate(choices):
    solver.push()
    bottom_books_letters = choice.split(', ')
    bottom_books_ids = [book_map[letter] for letter in bottom_books_letters]
    for book_id in bottom_books_ids:
        solver.add(book_shelf[book_id] == 2)
    solver.add(ForAll([b], Implies(And(b >= 0, b < 8), Implies(book_shelf[b] == 2, Or([b == id for id in bottom_books_ids])))))
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
