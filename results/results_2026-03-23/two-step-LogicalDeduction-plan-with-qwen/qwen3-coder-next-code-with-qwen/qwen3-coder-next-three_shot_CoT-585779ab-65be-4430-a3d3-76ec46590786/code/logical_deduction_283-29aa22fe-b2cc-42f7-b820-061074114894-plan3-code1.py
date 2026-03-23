from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain for three books
books = ["white", "green", "orange"]
positions = range(1, 4)
problem.addVariables(books, positions)

# Add constraints
# All books must be in different positions
problem.addConstraint(AllDifferentConstraint())

# The green book is to the right of the white book
problem.addConstraint(lambda w, g: g > w, ["white", "green"])

# The orange book is the rightmost (position 3)
problem.addConstraint(lambda o: o == 3, ["orange"])

# Solve for the arrangement
solutions = problem.getSolutions()

# Map choice letters to books
choices = {
    "A": "white",
    "B": "green",
    "C": "orange"
}

# Find which book is at position 2 (second from left)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 2:
            print(letter)