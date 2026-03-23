from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
books = ["white", "green", "orange"]
positions = range(1, 4)
problem.addVariables(books, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The green book is to the right of the white book"
problem.addConstraint(lambda white, green: white < green, ["white", "green"])

# "The orange book is the rightmost"
problem.addConstraint(lambda orange: orange == 3, ["orange"])

# Solve the problem
solutions = problem.getSolutions()

# Determine which book is leftmost (position 1)
choices = {
    "A": "white",
    "B": "green",
    "C": "orange"
}

# Find and print the correct choice
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 1:
            print(letter)