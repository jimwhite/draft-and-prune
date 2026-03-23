from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
books = ["orange", "white", "purple"]
positions = range(1, 4)
problem.addVariables(books, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The orange book is to the left of the white book"
problem.addConstraint(lambda orange, white: orange < white, ["orange", "white"])

# "The purple book is the rightmost"
problem.addConstraint(lambda purple: purple == 3, ["purple"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to book names
choices = {
    "A": "orange",
    "B": "white",
    "C": "purple"
}

# Find which book is in position 2 (second from left)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 2:
            print(letter)