from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (books) and domain (positions 1 to 7)
books = ["brown", "white", "black", "yellow", "orange", "blue", "green"]
positions = range(1, 8)
problem.addVariables(books, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "The yellow book is the rightmost" -> position 7
problem.addConstraint(lambda yellow: yellow == 7, ["yellow"])

# "The blue book is to the left of the orange book" -> blue < orange
problem.addConstraint(lambda blue, orange: blue < orange, ["blue", "orange"])

# "The green book is to the right of the white book" -> white < green
problem.addConstraint(lambda white, green: white < green, ["white", "green"])

# "The blue book is to the right of the green book" -> green < blue
problem.addConstraint(lambda green, blue: green < blue, ["green", "blue"])

# "The black book is the fourth from the left" -> position 4
problem.addConstraint(lambda black: black == 4, ["black"])

# "The brown book is the third from the right" -> position 5 (7 - 3 + 1 = 5)
problem.addConstraint(lambda brown: brown == 5, ["brown"])

# Solve the problem
solutions = problem.getSolutions()

# Get the first (and only) solution
solution = solutions[0]

# Map choice letters to book names
choices = {
    "A": "brown",
    "B": "white",
    "C": "black",
    "D": "yellow",
    "E": "orange",
    "F": "blue",
    "G": "green"
}

# Find which book is at position 1 (leftmost)
for letter, book_name in choices.items():
    if solution[book_name] == 1:
        print(letter)