from z3 import *

# Variables
book_shelf = Array('book_shelf', IntSort(), IntSort())
b = Int('b')
s = Int('s')

# Solver
solver = Solver()

# Constraints
solver.add(ForAll([b], And(book_shelf[b] >= 0, book_shelf[b] <= 2)))
solver.add(ForAll([s], Sum([If(book_shelf[b] == s, 1, 0) for b in range(8)]) >= 2))
solver.add(Sum([If(book_shelf[b] == 2, 1, 0) for b in range(8)]) > Sum([If(book_shelf[b] == 0, 1, 0) for b in range(8)]))
solver.add(book_shelf[3] == 1)
solver.add(book_shelf[4] < book_shelf[0])
solver.add(book_shelf[7] < book_shelf[5])
solver.add(book_shelf[0] == book_shelf[6])

# Answer choices and their corresponding constraints
answer_choices = [
    (book_shelf[7] < book_shelf[6], "A"),
    (book_shelf[4] < book_shelf[1], "B"),
    (book_shelf[3] < book_shelf[0], "C"),
    (book_shelf[1] < book_shelf[7], "D"),
    (book_shelf[0] < book_shelf[5], "E")
]

possible_answers = []

for constraint, letter in answer_choices:
    solver.push()
    solver.add(constraint)
    if solver.check() == sat:
        possible_answers.append((constraint, letter))
    solver.pop()

for constraint, letter in possible_answers:
    solver.push()
    solver.add(Not(constraint))
    if solver.check() == unsat:
        print(f"Option {letter} is correct")
        exit()
    solver.pop()