from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
books = ["yellow", "green", "gray", "blue", "orange"]
positions = range(1, 6)
problem.addVariables(books, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# Gray book is to the left of green book
problem.addConstraint(lambda gray, green: gray < green, ("gray", "green"))

# Gray book is second from the right (position 4)
problem.addConstraint(lambda gray: gray == 4, ("gray",))

# Yellow book is to the right of orange book
problem.addConstraint(lambda orange, yellow: orange < yellow, ("orange", "yellow"))

# Blue book is second from the left (position 2)
problem.addConstraint(lambda blue: blue == 2, ("blue",))

# Solve the problem
solutions = problem.getSolutions()

# Map choices to book names
choices = {
    "A": "yellow",
    "B": "green", 
    "C": "gray",
    "D": "blue",
    "E": "orange"
}

# Find which book is at position 3 (third from the left)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 3:
            print(letter)