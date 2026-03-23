from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables (books) and domain (positions 1 to 5, where 1 is leftmost)
books = ["yellow", "gray", "red", "black", "white"]
positions = range(1, 6)
problem.addVariables(books, positions)

# Add constraints based on the statements
# All books must be in unique positions
problem.addConstraint(AllDifferentConstraint())

# "The gray book is to the left of the yellow book"
problem.addConstraint(lambda g, y: g < y, ("gray", "yellow"))

# "The white book is to the left of the red book"
problem.addConstraint(lambda w, r: w < r, ("white", "red"))

# "The black book is to the right of the red book"
problem.addConstraint(lambda b, r: b > r, ("black", "red"))

# "The black book is to the left of the gray book"
problem.addConstraint(lambda b, g: b < g, ("black", "gray"))

# Solve for all valid arrangements
solutions = problem.getSolutions()

# Map books to choice letters based on the question's options
book_to_choice = {
    "yellow": "A",
    "gray": "B",
    "red": "C",
    "black": "D",
    "white": "E"
}

# Find the book at position 3 (third from the left)
for solution in solutions:
    for book, pos in solution.items():
        if pos == 3:
            print(book_to_choice[book])