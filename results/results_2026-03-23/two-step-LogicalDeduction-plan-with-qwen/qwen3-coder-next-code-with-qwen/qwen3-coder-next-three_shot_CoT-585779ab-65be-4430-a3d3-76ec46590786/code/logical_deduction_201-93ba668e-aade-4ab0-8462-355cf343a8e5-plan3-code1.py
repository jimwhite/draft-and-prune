from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (books) and domain (positions 1 to 7)
books = ["purple", "brown", "red", "blue", "gray", "black", "green"]
positions = range(1, 8)
problem.addVariables(books, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# "The brown book is to the left of the green book."
problem.addConstraint(lambda brown, green: brown < green, ["brown", "green"])

# "The gray book is the second from the left."
problem.addConstraint(lambda gray: gray == 2, ["gray"])

# "The black book is to the left of the gray book."
problem.addConstraint(lambda black, gray: black < gray, ["black", "gray"])

# "The blue book is to the left of the red book."
problem.addConstraint(lambda blue, red: blue < red, ["blue", "red"])

# "The blue book is the second from the right."
problem.addConstraint(lambda blue: blue == 6, ["blue"])

# "The green book is to the left of the purple book."
problem.addConstraint(lambda green, purple: green < purple, ["green", "purple"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to book names for the fourth position (position 4)
choices = {
    "A": "purple",
    "B": "brown",
    "C": "red",
    "D": "blue",
    "E": "gray",
    "F": "black",
    "G": "green"
}

# Find which book is at position 4 (fourth from the left)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 4:
            print(letter)