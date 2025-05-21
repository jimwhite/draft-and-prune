from z3 import *

# Variables
book_shelf = Array('book_shelf', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints
b = Int('b')
s = Int('s')
solver.add(ForAll([b], And(book_shelf[b] >= 0, book_shelf[b] <= 2))) # Constraint 0
solver.add(ForAll([s], Implies(And(s >= 0, s <= 2), Sum([If(book_shelf[i] == s, 1, 0) for i in range(8)]) >= 2))) # Constraint 1
solver.add(Sum([If(book_shelf[i] == 2, 1, 0) for i in range(8)]) > Sum([If(book_shelf[i] == 0, 1, 0) for i in range(8)])) # Constraint 2
solver.add(book_shelf[3] == 1) # Constraint 3
solver.add(book_shelf[4] < book_shelf[0]) # Constraint 4
solver.add(book_shelf[7] < book_shelf[5]) # Constraint 5
solver.add(book_shelf[0] == book_shelf[6]) # Constraint 6

# Answer choices
choices = [
    book_shelf[3] == book_shelf[6],  # A
    book_shelf[4] == book_shelf[1],  # B
    book_shelf[5] == book_shelf[0],  # C
    book_shelf[6] == book_shelf[2],  # D
    book_shelf[2] == book_shelf[7]   # E
]

for i, choice in enumerate(choices):
    solver.push()
    solver.add(choice)
    if solver.check() == sat:
        m = solver.model()
        values = [m.eval(book_shelf[j]) for j in range(8)]
        solver.pop()
        solver.push()
        solver.add(choice)
        solver.add(Or([book_shelf[j] != values[j] for j in range(8)]))
        if solver.check() == unsat:
            print(f"Option {chr(65 + i)} is correct")
            exit()
    solver.pop()
