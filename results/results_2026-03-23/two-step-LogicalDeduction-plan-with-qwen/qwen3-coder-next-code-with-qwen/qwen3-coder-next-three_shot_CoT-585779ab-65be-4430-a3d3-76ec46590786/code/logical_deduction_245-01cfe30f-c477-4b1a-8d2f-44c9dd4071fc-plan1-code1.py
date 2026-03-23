from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
books = ["orange", "yellow", "blue"]
positions = range(1, 4)
problem.addVariables(books, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The blue book is to the right of the yellow book"
problem.addConstraint(lambda yellow, blue: yellow < blue, ["yellow", "blue"])

# "The orange book is the second from the left"
problem.addConstraint(lambda orange: orange == 2, ["orange"])

# Solve for arrangements
solutions = problem.getSolutions()

# Map choice letters to book names
choices = {
    "A": "orange",
    "B": "yellow",
    "C": "blue"
}

# Find which book is rightmost (position 3)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 3:
            print(letter)