from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
books = ["orange", "white", "purple"]
positions = range(1, 4)
problem.addVariables(books, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The orange book is to the left of the white book."
problem.addConstraint(lambda orange, white: orange < white, ["orange", "white"])

# "The purple book is the rightmost."
problem.addConstraint(lambda purple: purple == 3, ["purple"])

# Solve for the arrangement
solutions = problem.getSolutions()

# Map choice letters to books
choices = {
    "A": "orange",
    "B": "white",
    "C": "purple"
}

# Find which book is second from the left (position 2)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 2:
            print(letter)