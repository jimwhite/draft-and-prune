from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
books = ["green", "blue", "white", "purple", "yellow"]
positions = range(1, 6)
problem.addVariables(books, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The blue book is to the right of the yellow book" -> blue > yellow
problem.addConstraint(lambda yellow, blue: yellow < blue, ["yellow", "blue"])

# "The white book is to the left of the yellow book" -> white < yellow
problem.addConstraint(lambda white, yellow: white < yellow, ["white", "yellow"])

# "The blue book is the second from the right" -> blue == 4
problem.addConstraint(lambda blue: blue == 4, ["blue"])

# "The purple book is the second from the left" -> purple == 2
problem.addConstraint(lambda purple: purple == 2, ["purple"])

# Solve for the arrangement
solutions = problem.getSolutions()

# Map choices to books
choices = {
    "A": "green",
    "B": "blue",
    "C": "white",
    "D": "purple",
    "E": "yellow"
}

# Find the leftmost book (position 1) and output corresponding choice letter
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 1:
            print(letter)