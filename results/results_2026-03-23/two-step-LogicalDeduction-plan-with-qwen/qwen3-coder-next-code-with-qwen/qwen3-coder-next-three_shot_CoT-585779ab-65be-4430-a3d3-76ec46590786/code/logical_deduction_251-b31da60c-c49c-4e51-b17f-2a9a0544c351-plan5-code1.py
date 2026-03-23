from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
books = ["purple", "white", "blue"]
positions = range(1, 4)
problem.addVariables(books, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# Purple is to the left of blue: purple < blue
problem.addConstraint(lambda purple, blue: purple < blue, ["purple", "blue"])

# Purple is to the right of white: white < purple
problem.addConstraint(lambda white, purple: white < purple, ["white", "purple"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to books
choices = {
    "A": "purple",
    "B": "white",
    "C": "blue"
}

# Find which book is rightmost (position 3)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 3:
            print(letter)