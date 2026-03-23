from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
books = ["orange", "white", "purple"]
positions = range(1, 4)
problem.addVariables(books, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# The orange book is to the left of the white book
problem.addConstraint(lambda orange, white: orange < white, ["orange", "white"])

# The purple book is the rightmost
problem.addConstraint(lambda purple: purple == 3, ["purple"])

# Solve the problem
solutions = problem.getSolutions()

# Determine which book is second from the left (position 2)
choices = {
    "A": "orange",
    "B": "white",
    "C": "purple"
}

# Find the book at position 2 and print its corresponding choice letter
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 2:
            print(letter)