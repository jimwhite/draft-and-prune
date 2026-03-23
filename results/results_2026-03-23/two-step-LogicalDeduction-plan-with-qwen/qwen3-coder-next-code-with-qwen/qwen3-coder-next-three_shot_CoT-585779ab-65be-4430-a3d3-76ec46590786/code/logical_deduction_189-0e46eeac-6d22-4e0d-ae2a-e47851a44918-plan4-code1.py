from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (books) and domain (positions 1 to 7)
books = ["orange", "green", "red", "gray", "purple", "blue", "brown"]
positions = range(1, 8)
problem.addVariables(books, positions)

# Add AllDifferent constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem statements
# "The purple book is the fourth from the left"
problem.addConstraint(lambda purple: purple == 4, ["purple"])

# "The brown book is the third from the left"
problem.addConstraint(lambda brown: brown == 3, ["brown"])

# "The green book is to the left of the blue book"
problem.addConstraint(lambda green, blue: green < blue, ["green", "blue"])

# "The red book is the leftmost"
problem.addConstraint(lambda red: red == 1, ["red"])

# "The gray book is the third from the right" (position = 7 - 3 + 1 = 5)
problem.addConstraint(lambda gray: gray == 5, ["gray"])

# "The orange book is the rightmost"
problem.addConstraint(lambda orange: orange == 7, ["orange"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to book names
choices = {
    "A": "orange",
    "B": "green",
    "C": "red",
    "D": "gray",
    "E": "purple",
    "F": "blue",
    "G": "brown"
}

# Find which book is at position 4 (fourth from the left)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 4:
            print(letter)