from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (books) and domain (positions 1 to 5, left to right)
books = ["green", "blue", "white", "purple", "yellow"]
positions = range(1, 6)
problem.addVariables(books, positions)

# Add constraints
# All books must be in different positions
problem.addConstraint(AllDifferentConstraint())

# Blue book is to the right of the yellow book: blue > yellow
problem.addConstraint(lambda blue, yellow: blue > yellow, ("blue", "yellow"))

# White book is to the left of the yellow book: white < yellow
problem.addConstraint(lambda white, yellow: white < yellow, ("white", "yellow"))

# Blue book is the second from the right: blue == 4
problem.addConstraint(lambda blue: blue == 4, ("blue",))

# Purple book is the second from the left: purple == 2
problem.addConstraint(lambda purple: purple == 2, ("purple",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to book names for position 2 (second from left)
choices = {
    "A": "green",
    "B": "blue",
    "C": "white",
    "D": "purple",
    "E": "yellow"
}

# Find which book is at position 2 and print the corresponding letter
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 2:
            print(letter)