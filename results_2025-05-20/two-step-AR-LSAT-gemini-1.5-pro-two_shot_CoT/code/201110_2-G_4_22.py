from z3 import *

# Variables
book_shelf = Array('book_shelf', IntSort(), IntSort())

# Solver
solver = Solver()

# Book to ID mapping (F=0, G=1, H=2, I=3, K=4, L=5, M=6, O=7)
book_ids = {'F': 0, 'G': 1, 'H': 2, 'I': 3, 'K': 4, 'L': 5, 'M': 6, 'O': 7}

# Constraint 1: Domain
b = Int('b')
solver.add(ForAll([b], And(book_shelf[b] >= 0, book_shelf[b] <= 2)))

# Constraint 2: Two books minimum per shelf
for shelf in range(3):
    solver.add(sum([If(book_shelf[i] == shelf, 1, 0) for i in range(8)]) >= 2)

# Constraint 3: Bottom > Top
solver.add(sum([If(book_shelf[i] == 2, 1, 0) for i in range(8)]) > sum([If(book_shelf[i] == 0, 1, 0) for i in range(8)]))

# Constraint 4: I on Middle
solver.add(book_shelf[book_ids['I']] == 1)

# Constraint 5: K above F
solver.add(book_shelf[book_ids['K']] < book_shelf[book_ids['F']])

# Constraint 6: O above L
solver.add(book_shelf[book_ids['O']] < book_shelf[book_ids['L']])

# Constraint 7: F same as M
solver.add(book_shelf[book_ids['F']] == book_shelf[book_ids['M']])

# Constraint 8: G on Top (Question Condition)
solver.add(book_shelf[book_ids['G']] == 0)

# Answer Choices
choices = [
    ["H", "I"],
    ["I", "L"],
    ["H", "I", "L"],
    ["I", "K", "L"],
    ["F", "I", "M"]
]

# Check each answer choice
for i, choice in enumerate(choices):
    solver.push()
    for book in choice:
        solver.add(book_shelf[book_ids[book]] == 1)
    for book in book_ids:
        if book not in choice:
            solver.add(book_shelf[book_ids[book]] != 1)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()