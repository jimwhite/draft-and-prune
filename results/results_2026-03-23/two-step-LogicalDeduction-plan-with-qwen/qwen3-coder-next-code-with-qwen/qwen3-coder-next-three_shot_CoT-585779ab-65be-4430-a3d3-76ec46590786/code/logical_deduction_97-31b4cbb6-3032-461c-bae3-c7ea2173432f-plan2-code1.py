from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (books) and domain (positions 1 to 5)
books = ["blue", "red", "brown", "yellow", "orange"]
positions = range(1, 6)
problem.addVariables(books, positions)

# Add constraints
# All books must be in different positions
problem.addConstraint(AllDifferentConstraint())

# "The red book is to the left of the brown book"
problem.addConstraint(lambda red, brown: red < brown, ["red", "brown"])

# "The yellow book is to the right of the orange book"
problem.addConstraint(lambda orange, yellow: orange < yellow, ["orange", "yellow"])

# "The brown book is the second from the left"
problem.addConstraint(lambda brown: brown == 2, ["brown"])

# "The yellow book is to the left of the blue book"
problem.addConstraint(lambda yellow, blue: yellow < blue, ["yellow", "blue"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to books
choices = {
    "A": "blue",
    "B": "red",
    "C": "brown",
    "D": "yellow",
    "E": "orange"
}

# Find which book is in position 3 (third from the left)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 3:
            print(letter)