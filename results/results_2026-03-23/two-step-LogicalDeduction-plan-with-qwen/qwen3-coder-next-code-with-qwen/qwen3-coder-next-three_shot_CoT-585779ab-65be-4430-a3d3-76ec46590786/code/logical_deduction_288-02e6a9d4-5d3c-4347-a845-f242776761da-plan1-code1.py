from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
books = ["purple", "white", "blue"]
positions = range(1, 4)  # 1=leftmost, 2=middle, 3=rightmost
problem.addVariables(books, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The purple book is to the left of the blue book" => purple < blue
problem.addConstraint(lambda purple, blue: purple < blue, ["purple", "blue"])

# "The purple book is to the right of the white book" => purple > white
problem.addConstraint(lambda purple, white: purple > white, ["purple", "white"])

# Solve the problem
solutions = problem.getSolutions()

# Determine which book is leftmost (position 1)
leftmost_book = None
for solution in solutions:
    for book, pos in solution.items():
        if pos == 1:
            leftmost_book = book
            break
    if leftmost_book is not None:
        break

# Map to choice letters
if leftmost_book == "white":
    print("B")
elif leftmost_book == "purple":
    print("A")
elif leftmost_book == "blue":
    print("C")