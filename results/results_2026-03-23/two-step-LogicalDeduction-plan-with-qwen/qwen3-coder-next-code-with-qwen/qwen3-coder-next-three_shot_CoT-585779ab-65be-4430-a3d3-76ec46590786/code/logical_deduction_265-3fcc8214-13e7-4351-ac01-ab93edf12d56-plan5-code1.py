from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
books = ["brown", "yellow", "orange"]
positions = range(1, 4)
problem.addVariables(books, positions)

# Add AllDifferent constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# "The yellow book is the leftmost"
problem.addConstraint(lambda yellow: yellow == 1, ["yellow"])

# "The orange book is to the right of the brown book"
problem.addConstraint(lambda brown, orange: brown < orange, ["brown", "orange"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to books
choices = {
    "A": "brown",
    "B": "yellow",
    "C": "orange"
}

# Find which book is in position 2 (second from the left)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 2:
            print(letter)