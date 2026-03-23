from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
books = ["purple", "red", "yellow"]
positions = range(1, 4)
problem.addVariables(books, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The purple book is to the right of the yellow book" -> purple > yellow
problem.addConstraint(lambda purple, yellow: purple > yellow, ["purple", "yellow"])

# "The yellow book is to the right of the red book" -> yellow > red
problem.addConstraint(lambda yellow, red: yellow > red, ["yellow", "red"])

# Solve the problem
solutions = problem.getSolutions()

# Determine which book is leftmost (position 1)
leftmost_book = None
for solution in solutions:
    for book, pos in solution.items():
        if pos == 1:
            leftmost_book = book
            break

# Map to choice letters
if leftmost_book == "red":
    print("B")
elif leftmost_book == "yellow":
    print("C")
elif leftmost_book == "purple":
    print("A")