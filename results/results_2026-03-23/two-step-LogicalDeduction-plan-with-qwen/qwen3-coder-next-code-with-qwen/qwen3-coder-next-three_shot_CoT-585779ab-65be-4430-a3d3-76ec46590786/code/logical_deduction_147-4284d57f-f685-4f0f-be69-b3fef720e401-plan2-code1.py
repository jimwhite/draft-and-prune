from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (books) and domain (positions 1 to 7)
books = ["brown", "yellow", "black", "white", "green", "orange", "purple"]
positions = range(1, 8)
problem.addVariables(books, positions)

# Add all different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem description
# Purple book is rightmost (position 7)
problem.addConstraint(lambda purple: purple == 7, ["purple"])

# Yellow book is leftmost (position 1)
problem.addConstraint(lambda yellow: yellow == 1, ["yellow"])

# Orange book is second from the right (position 6)
problem.addConstraint(lambda orange: orange == 6, ["orange"])

# Brown book is to the left of green book (brown < green)
problem.addConstraint(lambda brown, green: brown < green, ["brown", "green"])

# Brown book is to the right of black book (black < brown)
problem.addConstraint(lambda black, brown: black < brown, ["black", "brown"])

# White book is fourth from the left (position 4)
problem.addConstraint(lambda white: white == 4, ["white"])

# Solve the problem
solutions = problem.getSolutions()

# In a 7-position shelf, third from the right is position 5
third_from_right_pos = 5

# Map choice letters to book names
choices = {
    "A": "brown",
    "B": "yellow",
    "C": "black",
    "D": "white",
    "E": "green",
    "F": "orange",
    "G": "purple"
}

# Find which book is at position 5 and print the corresponding choice letter
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == third_from_right_pos:
            print(letter)