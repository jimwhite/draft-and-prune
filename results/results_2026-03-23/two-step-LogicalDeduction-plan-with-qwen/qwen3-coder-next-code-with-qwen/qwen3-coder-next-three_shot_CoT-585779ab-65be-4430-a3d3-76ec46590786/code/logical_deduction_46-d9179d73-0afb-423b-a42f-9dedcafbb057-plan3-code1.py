from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
books = ["yellow", "green", "gray", "blue", "orange"]
positions = range(1, 6)
problem.addVariables(books, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# Gray is to the left of green
problem.addConstraint(lambda gray, green: gray < green, ("gray", "green"))

# Gray is second from the right (position 4)
problem.addConstraint(lambda gray: gray == 4, ("gray",))

# Yellow is to the right of orange
problem.addConstraint(lambda orange, yellow: orange < yellow, ("orange", "yellow"))

# Blue is second from the left (position 2)
problem.addConstraint(lambda blue: blue == 2, ("blue",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to book names for rightmost position (position 5)
choices = {
    "A": "yellow",
    "B": "green",
    "C": "gray",
    "D": "blue",
    "E": "orange"
}

# Find which book is at position 5 (rightmost)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 5:
            print(letter)