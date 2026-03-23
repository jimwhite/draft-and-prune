from constraint import *

# Initialize the problem
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

# Map choices to book names
choices = {
    "A": "gray",
    "B": "purple",
    "C": "red"
}

# Find which book is in position 2 (second from the left)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 2:
            print(letter)