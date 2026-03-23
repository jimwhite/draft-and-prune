from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (the seven books)
books = ["orange", "green", "red", "gray", "purple", "blue", "brown"]

# Define domain: positions 1 to 7 (1 = leftmost, 7 = rightmost)
positions = range(1, 8)

# Add variables with their domain
problem.addVariables(books, positions)

# Add constraint that all books must be in different positions
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "The purple book is the fourth from the left"
problem.addConstraint(lambda purple: purple == 4, ["purple"])

# "The brown book is the third from the left"
problem.addConstraint(lambda brown: brown == 3, ["brown"])

# "The green book is to the left of the blue book"
problem.addConstraint(lambda green, blue: green < blue, ["green", "blue"])

# "The red book is the leftmost"
problem.addConstraint(lambda red: red == 1, ["red"])

# "The gray book is the third from the right" (position = 7 - 3 + 1 = 5)
problem.addConstraint(lambda gray: gray == 5, ["gray"])

# "The orange book is the rightmost"
problem.addConstraint(lambda orange: orange == 7, ["orange"])

# Solve the problem
solutions = problem.getSolutions()

# Get the unique solution (there should be only one)
solution = solutions[0]

# Determine which book is at position 4 (fourth from the left)
book_at_position_4 = None
for book, pos in solution.items():
    if pos == 4:
        book_at_position_4 = book
        break

# Map books to choice letters
choices = {
    "A": "orange",
    "B": "green",
    "C": "red",
    "D": "gray",
    "E": "purple",
    "F": "blue",
    "G": "brown"
}

# Find the choice letter corresponding to the book at position 4
for letter, book_name in choices.items():
    if book_name == book_at_position_4:
        print(letter)
        break