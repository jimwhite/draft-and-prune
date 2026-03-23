from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (books) and domain (positions 1 to 5, where 1 is leftmost)
books = ["yellow", "green", "gray", "blue", "orange"]
positions = range(1, 6)
problem.addVariables(books, positions)

# Add constraints based on the problem statements
# All books must be in different positions
problem.addConstraint(AllDifferentConstraint())

# Gray book is to the left of green book: gray < green
problem.addConstraint(lambda gray, green: gray < green, ["gray", "green"])

# Gray book is second from the right: position 4
problem.addConstraint(lambda gray: gray == 4, ["gray"])

# Yellow book is to the right of orange book: orange < yellow
problem.addConstraint(lambda orange, yellow: orange < yellow, ["orange", "yellow"])

# Blue book is second from the left: position 2
problem.addConstraint(lambda blue: blue == 2, ["blue"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to book names for the question about third from left (position 3)
choices = {
    "A": "yellow",
    "B": "green",
    "C": "gray",
    "D": "blue",
    "E": "orange"
}

# Find which book is at position 3 and print the corresponding choice letter
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 3:
            print(letter)