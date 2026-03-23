from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
books = ["gray", "red", "yellow", "blue", "orange"]
positions = range(1, 6)
problem.addVariables(books, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# Gray is to the right of yellow: gray > yellow
problem.addConstraint(lambda gray, yellow: gray > yellow, ("gray", "yellow"))

# Orange is to the right of red: orange > red
problem.addConstraint(lambda orange, red: orange > red, ("orange", "red"))

# Blue is the rightmost: blue == 5
problem.addConstraint(lambda blue: blue == 5, ("blue",))

# Gray is to the left of red: gray < red
problem.addConstraint(lambda gray, red: gray < red, ("gray", "red"))

# Solve the problem
solutions = problem.getSolutions()

# Map choices to book names
choices = {
    "A": "gray",
    "B": "red",
    "C": "yellow",
    "D": "blue",
    "E": "orange"
}

# Find the leftmost book (position 1) and print corresponding choice letter
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 1:
            print(letter)