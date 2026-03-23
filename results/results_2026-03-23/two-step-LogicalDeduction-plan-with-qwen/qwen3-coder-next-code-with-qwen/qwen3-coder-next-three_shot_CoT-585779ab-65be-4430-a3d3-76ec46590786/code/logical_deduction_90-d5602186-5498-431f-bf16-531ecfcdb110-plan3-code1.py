from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
books = ["green", "orange", "gray", "yellow", "purple"]
positions = range(1, 6)
problem.addVariables(books, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The green book is the rightmost" -> position 5
problem.addConstraint(lambda green: green == 5, ["green"])

# "The gray book is to the right of the orange book" -> orange < gray
problem.addConstraint(lambda orange, gray: orange < gray, ["orange", "gray"])

# "The purple book is to the left of the yellow book" -> purple < yellow
problem.addConstraint(lambda purple, yellow: purple < yellow, ["purple", "yellow"])

# "The purple book is to the right of the gray book" -> gray < purple
problem.addConstraint(lambda gray, purple: gray < purple, ["gray", "purple"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to book names
choices = {
    "A": "green",
    "B": "orange",
    "C": "gray",
    "D": "yellow",
    "E": "purple"
}

# Find which book is in position 3 (third from the left)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 3:
            print(letter)