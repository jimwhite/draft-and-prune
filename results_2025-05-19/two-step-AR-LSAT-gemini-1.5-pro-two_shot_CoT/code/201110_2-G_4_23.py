from z3 import *

# Variables
book_shelf = Array('book_shelf', IntSort(), IntSort())
b = Int('b')
s = Int('s')

# Solver
solver = Solver()

# Constraints
solver.add(ForAll([b], Implies(And(b >= 0, b <= 7), And(book_shelf[b] >= 0, book_shelf[b] <= 2)))) # Constraint 0
solver.add(ForAll([s], Implies(And(s >= 0, s <= 2), Sum([If(book_shelf[b] == s, 1, 0) for b in range(8)]) >= 2))) # Constraint 1
solver.add(Sum([If(book_shelf[b] == 2, 1, 0) for b in range(8)]) > Sum([If(book_shelf[b] == 0, 1, 0) for b in range(8)])) # Constraint 2
solver.add(book_shelf[3] == 1) # Constraint 3
solver.add(book_shelf[4] < book_shelf[0]) # Constraint 4
solver.add(book_shelf[7] < book_shelf[5]) # Constraint 5
solver.add(book_shelf[0] == book_shelf[6]) # Constraint 6
solver.add(book_shelf[5] < book_shelf[2]) # Constraint 7

# Answer choices and their negations
answer_choices = [
    (0, 1, book_shelf[0] != book_shelf[1]),  # A: F and G are placed on the same shelf as each other.
    (1, 2, book_shelf[1] != book_shelf[2]),  # B: G and H are placed on the same shelf as each other.
    (2, 6, book_shelf[2] != book_shelf[6]),  # C: H and M are placed on the same shelf as each other.
    (3, 1, book_shelf[3] != book_shelf[1]),  # D: I and G are placed on the same shelf as each other.
    (4, 7, book_shelf[4] != book_shelf[7])   # E: K and O are placed on the same shelf as each other.
]

# Check each answer choice
for i, (book1, book2, negation) in enumerate(answer_choices):
    solver.push()
    solver.add(negation)
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()