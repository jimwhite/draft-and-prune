from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
books = ["gray", "orange", "brown"]
positions = range(1, 4)
problem.addVariables(books, positions)

# Add constraints
# All books must be in different positions
problem.addConstraint(AllDifferentConstraint())

# The orange book is the leftmost (position 1)
problem.addConstraint(lambda orange: orange == 1, ["orange"])

# The gray book is to the right of the brown book (brown < gray)
problem.addConstraint(lambda brown, gray: brown < gray, ["brown", "gray"])

# Solve for the arrangement
solutions = problem.getSolutions()

# Map choice letters to books
choices = {
    "A": "gray",
    "B": "orange",
    "C": "brown"
}

# Find which book is rightmost (position 3)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 3:
            print(letter)