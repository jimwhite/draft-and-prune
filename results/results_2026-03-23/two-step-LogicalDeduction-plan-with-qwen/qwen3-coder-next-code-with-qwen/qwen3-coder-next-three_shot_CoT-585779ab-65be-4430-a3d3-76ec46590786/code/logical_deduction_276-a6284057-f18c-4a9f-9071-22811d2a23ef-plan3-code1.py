from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
books = ["purple", "red", "yellow"]
positions = range(1, 4)
problem.addVariables(books, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# The purple book is to the right of the yellow book: purple > yellow
problem.addConstraint(lambda purple, yellow: purple > yellow, ["purple", "yellow"])

# The yellow book is to the right of the red book: yellow > red
problem.addConstraint(lambda yellow, red: yellow > red, ["yellow", "red"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to books
choices = {
    "A": "purple",
    "B": "red",
    "C": "yellow"
}

# Find the leftmost book (position 1) and print corresponding choice letter
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 1:
            print(letter)