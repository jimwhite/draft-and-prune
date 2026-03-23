from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
books = ["white", "green", "orange"]
positions = range(1, 4)
problem.addVariables(books, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The green book is to the right of the white book"
problem.addConstraint(lambda white, green: white < green, ["white", "green"])

# "The orange book is the rightmost"
problem.addConstraint(lambda orange: orange == 3, ["orange"])

# Solve for the arrangement
solutions = problem.getSolutions()

# Determine the correct answer (second from left means position 2)
choices = {
    "A": "white",
    "B": "green",
    "C": "orange"
}

# Find which book is at position 2
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 2:
            print(letter)