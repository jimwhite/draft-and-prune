from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
books = ["gray", "orange", "brown"]
positions = range(1, 4)
problem.addVariables(books, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The orange book is the leftmost"
problem.addConstraint(lambda orange: orange == 1, ["orange"])

# "The gray book is to the right of the brown book"
problem.addConstraint(lambda brown, gray: brown < gray, ["brown", "gray"])

# Solve the problem
solutions = problem.getSolutions()

# Map rightmost book to choice letter
choices = {
    "A": "gray",
    "B": "orange",
    "C": "brown"
}

# Find the rightmost book (position 3) and print corresponding letter
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 3:
            print(letter)