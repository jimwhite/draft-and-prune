from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain for three books
books = ["red", "gray", "white"]
positions = range(1, 4)
problem.addVariables(books, positions)

# Add constraints
# All books must be in different positions
problem.addConstraint(AllDifferentConstraint())

# The white book is to the left of the gray book
problem.addConstraint(lambda white, gray: white < gray, ("white", "gray"))

# The red book is the second from the left
problem.addConstraint(lambda red: red == 2, ("red",))

# Solve for the arrangement
solutions = problem.getSolutions()

# Determine which book is leftmost (position 1)
choices = {
    "A": "red",
    "B": "gray",
    "C": "white"
}

# Find and print the correct choice
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 1:
            print(letter)