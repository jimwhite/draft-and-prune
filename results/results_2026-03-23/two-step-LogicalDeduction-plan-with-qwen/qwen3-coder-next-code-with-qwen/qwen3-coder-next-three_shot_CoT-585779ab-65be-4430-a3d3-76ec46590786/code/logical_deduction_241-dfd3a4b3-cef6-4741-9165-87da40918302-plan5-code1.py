from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
books = ["gray", "purple", "red"]
positions = range(1, 4)
problem.addVariables(books, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# The purple book is to the left of the red book
problem.addConstraint(lambda purple, red: purple < red, ["purple", "red"])

# The gray book is to the left of the purple book
problem.addConstraint(lambda gray, purple: gray < purple, ["gray", "purple"])

# Solve the problem
solutions = problem.getSolutions()

# Determine which book is second from the left (position 2)
choices = {
    "A": "gray",
    "B": "purple",
    "C": "red"
}

# Find the correct choice
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 2:
            print(letter)