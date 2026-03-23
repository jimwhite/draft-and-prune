from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain for three books
books = ["purple", "white", "blue"]
positions = range(1, 4)
problem.addVariables(books, positions)

# Add constraints
# All books must be in different positions
problem.addConstraint(AllDifferentConstraint())

# "The purple book is to the left of the blue book" → purple < blue
problem.addConstraint(lambda purple, blue: purple < blue, ["purple", "blue"])

# "The purple book is to the right of the white book" → white < purple
problem.addConstraint(lambda white, purple: white < purple, ["white", "purple"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to book names
choices = {
    "A": "purple",
    "B": "white",
    "C": "blue"
}

# Find which book is at position 3 (rightmost)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 3:
            print(letter)