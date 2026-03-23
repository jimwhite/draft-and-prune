from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
books = ["white", "black", "purple"]
positions = range(1, 4)
problem.addVariables(books, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())
problem.addConstraint(lambda black, purple: black < purple, ["black", "purple"])
problem.addConstraint(lambda purple, white: purple < white, ["purple", "white"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to books
choices = {
    "A": "white",
    "B": "black",
    "C": "purple"
}

# Find which book is rightmost (position 3)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 3:
            print(letter)