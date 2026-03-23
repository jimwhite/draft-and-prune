from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables and domain for three books
books = ["white", "green", "orange"]
positions = range(1, 4)
problem.addVariables(books, positions)

# Add constraints
# All books must be in different positions
problem.addConstraint(AllDifferentConstraint())

# The green book is to the right of the white book (white < green)
problem.addConstraint(lambda white, green: white < green, ["white", "green"])

# The orange book is the rightmost (position 3)
problem.addConstraint(lambda orange: orange == 3, ["orange"])

# Solve for the unique arrangement
solutions = problem.getSolutions()
solution = solutions[0]

# Determine which book is second from the left (position 2)
choices = {
    "A": "white",
    "B": "green",
    "C": "orange"
}

# Find the book at position 2 and print its corresponding letter
for letter, book_name in choices.items():
    if solution[book_name] == 2:
        print(letter)