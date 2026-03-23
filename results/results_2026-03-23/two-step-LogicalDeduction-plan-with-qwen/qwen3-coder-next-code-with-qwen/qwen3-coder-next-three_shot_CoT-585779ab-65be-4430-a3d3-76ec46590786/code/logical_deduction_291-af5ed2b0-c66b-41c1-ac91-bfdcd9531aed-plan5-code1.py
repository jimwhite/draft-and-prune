from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
books = ["blue", "orange", "green"]
positions = range(1, 4)
problem.addVariables(books, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The green book is the leftmost"
problem.addConstraint(lambda green: green == 1, ["green"])

# "The orange book is to the left of the blue book"
problem.addConstraint(lambda orange, blue: orange < blue, ["orange", "blue"])

# Solve for the arrangement
solutions = problem.getSolutions()

# Determine the correct answer
choices = {
    "A": "blue",
    "B": "orange",
    "C": "green"
}

# Find which book is at position 3 (rightmost)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 3:
            print(letter)