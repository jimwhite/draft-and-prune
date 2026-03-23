from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
books = ["red", "gray", "white"]
positions = range(1, 4)
problem.addVariables(books, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The white book is to the left of the gray book"
problem.addConstraint(lambda white, gray: white < gray, ["white", "gray"])

# "The red book is the second from the left"
problem.addConstraint(lambda red: red == 2, ["red"])

# Solve for the unique arrangement
solutions = problem.getSolutions()
solution = solutions[0]

# Determine which book is leftmost (position 1)
leftmost_book = None
for book, pos in solution.items():
    if pos == 1:
        leftmost_book = book
        break

# Map to choice letters
if leftmost_book == "red":
    print("A")
elif leftmost_book == "gray":
    print("B")
elif leftmost_book == "white":
    print("C")