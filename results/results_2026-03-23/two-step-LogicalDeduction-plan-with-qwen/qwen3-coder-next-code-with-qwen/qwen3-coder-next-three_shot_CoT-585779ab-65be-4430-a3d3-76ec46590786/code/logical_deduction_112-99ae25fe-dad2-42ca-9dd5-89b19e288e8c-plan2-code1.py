from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (books) and domain (positions 1 to 7)
books = ["brown", "gray", "orange", "green", "black", "purple", "yellow"]
positions = range(1, 8)
problem.addVariables(books, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# "The purple book is the leftmost" -> purple == 1
problem.addConstraint(lambda purple: purple == 1, ["purple"])

# "The brown book is to the right of the yellow book" -> brown > yellow
problem.addConstraint(lambda brown, yellow: brown > yellow, ["brown", "yellow"])

# "The green book is to the left of the orange book" -> green < orange
problem.addConstraint(lambda green, orange: green < orange, ["green", "orange"])

# "The orange book is to the left of the gray book" -> orange < gray
problem.addConstraint(lambda orange, gray: orange < gray, ["orange", "gray"])

# "The black book is the third from the left" -> black == 3
problem.addConstraint(lambda black: black == 3, ["black"])

# "The green book is the third from the right" -> position = 7 - 2 = 5
problem.addConstraint(lambda green: green == 5, ["green"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to book names
choices = {
    "A": "brown",
    "B": "gray",
    "C": "orange",
    "D": "green",
    "E": "black",
    "F": "purple",
    "G": "yellow"
}

# Find which book is at position 5 (third from the right)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 5:
            print(letter)