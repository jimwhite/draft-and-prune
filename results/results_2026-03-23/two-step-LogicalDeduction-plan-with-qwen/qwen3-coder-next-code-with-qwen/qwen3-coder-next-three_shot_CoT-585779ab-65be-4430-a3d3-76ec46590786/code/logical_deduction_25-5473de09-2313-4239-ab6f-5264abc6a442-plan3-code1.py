from constraint import *

# Set up the problem
problem = Problem()

# Define variables and domain
books = ["blue", "purple", "yellow", "black", "green"]
positions = range(1, 6)
problem.addVariables(books, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The purple book is the third from the left"
problem.addConstraint(lambda purple: purple == 3, ["purple"])

# "The yellow book is to the left of the black book"
problem.addConstraint(lambda yellow, black: yellow < black, ["yellow", "black"])

# "The green book is to the left of the purple book"
problem.addConstraint(lambda green, purple: green < purple, ["green", "purple"])

# "The blue book is to the left of the green book"
problem.addConstraint(lambda blue, green: blue < green, ["blue", "green"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to book names
choices = {
    "A": "blue",
    "B": "purple",
    "C": "yellow",
    "D": "black",
    "E": "green"
}

# Find which book is in position 4 (second from the right)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 4:
            print(letter)