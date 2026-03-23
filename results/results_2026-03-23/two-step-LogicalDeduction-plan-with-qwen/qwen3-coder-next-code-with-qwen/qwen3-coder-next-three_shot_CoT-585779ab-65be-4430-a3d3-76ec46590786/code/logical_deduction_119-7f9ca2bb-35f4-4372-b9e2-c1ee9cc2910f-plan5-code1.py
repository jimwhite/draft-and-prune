from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (books) and domain (positions 1 to 7)
books = ["brown", "yellow", "black", "white", "green", "orange", "purple"]
positions = range(1, 8)
problem.addVariables(books, positions)

# Enforce uniqueness
problem.addConstraint(AllDifferentConstraint())

# Fixed position constraints
problem.addConstraint(lambda purple: purple == 7, ["purple"])
problem.addConstraint(lambda yellow: yellow == 1, ["yellow"])
problem.addConstraint(lambda orange: orange == 6, ["orange"])
problem.addConstraint(lambda white: white == 4, ["white"])

# Relative order constraints
problem.addConstraint(lambda brown, green: brown < green, ["brown", "green"])
problem.addConstraint(lambda black, brown: black < brown, ["black", "brown"])

# Solve the problem
solutions = problem.getSolutions()
solution = solutions[0]

# Map books to choice letters for position 3
book_to_choice = {
    "brown": "A",
    "yellow": "B",
    "black": "C",
    "white": "D",
    "green": "E",
    "orange": "F",
    "purple": "G"
}

# Find which book is at position 3
for book, pos in solution.items():
    if pos == 3:
        print(book_to_choice[book])