from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (the three books) and domain (positions 1 to 3)
books = ["brown", "yellow", "orange"]
positions = range(1, 4)
problem.addVariables(books, positions)

# Add constraints based on the statements
# All books must be in different positions
problem.addConstraint(AllDifferentConstraint())

# "The yellow book is the leftmost" -> position 1
problem.addConstraint(lambda yellow: yellow == 1, ["yellow"])

# "The orange book is to the right of the brown book" -> brown < orange
problem.addConstraint(lambda brown, orange: brown < orange, ["brown", "orange"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to books for the question about second from left (position 2)
choices = {
    "A": "brown",
    "B": "yellow",
    "C": "orange"
}

# Find which book is at position 2 and print the corresponding letter
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 2:
            print(letter)