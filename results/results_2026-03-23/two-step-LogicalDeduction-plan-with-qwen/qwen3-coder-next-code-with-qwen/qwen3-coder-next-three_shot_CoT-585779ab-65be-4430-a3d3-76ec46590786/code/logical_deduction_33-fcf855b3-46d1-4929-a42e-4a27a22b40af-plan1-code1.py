from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
books = ["gray", "red", "yellow", "blue", "orange"]
positions = range(1, 6)
problem.addVariables(books, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# "The gray book is to the right of the yellow book" → gray > yellow
problem.addConstraint(lambda gray, yellow: gray > yellow, ("gray", "yellow"))

# "The orange book is to the right of the red book" → orange > red
problem.addConstraint(lambda orange, red: orange > red, ("orange", "red"))

# "The blue book is the rightmost" → blue == 5
problem.addConstraint(lambda blue: blue == 5, ("blue",))

# "The gray book is to the left of the red book" → gray < red
problem.addConstraint(lambda gray, red: gray < red, ("gray", "red"))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to book names
choices = {
    "A": "gray",
    "B": "red",
    "C": "yellow",
    "D": "blue",
    "E": "orange"
}

# Find the leftmost book (position 1) and output corresponding choice letter
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 1:
            print(letter)