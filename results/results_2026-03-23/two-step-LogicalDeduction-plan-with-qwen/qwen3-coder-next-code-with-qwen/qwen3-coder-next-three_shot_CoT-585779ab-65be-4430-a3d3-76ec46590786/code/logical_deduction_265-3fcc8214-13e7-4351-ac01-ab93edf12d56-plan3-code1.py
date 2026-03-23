from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
books = ["brown", "yellow", "orange"]
positions = range(1, 4)
problem.addVariables(books, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The yellow book is the leftmost"
problem.addConstraint(lambda yellow: yellow == 1, ["yellow"])

# "The orange book is to the right of the brown book"
problem.addConstraint(lambda brown, orange: brown < orange, ["brown", "orange"])

# Solve the problem
solutions = problem.getSolutions()

# Determine which book is second from the left (position 2)
choices = {
    "A": "brown",
    "B": "yellow",
    "C": "orange"
}

# Find the correct choice
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 2:
            print(letter)