from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
books = ["gray", "red", "yellow", "blue", "orange"]
positions = range(1, 6)
problem.addVariables(books, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The gray book is to the right of the yellow book"
problem.addConstraint(lambda gray, yellow: gray > yellow, ("gray", "yellow"))

# "The orange book is to the right of the red book"
problem.addConstraint(lambda orange, red: orange > red, ("orange", "red"))

# "The blue book is the rightmost"
problem.addConstraint(lambda blue: blue == 5, ("blue",))

# "The gray book is to the left of the red book"
problem.addConstraint(lambda gray, red: gray < red, ("gray", "red"))

# Solve for the arrangement
solutions = problem.getSolutions()

# Map choice letters to book names
choices = {
    "A": "gray",
    "B": "red",
    "C": "yellow",
    "D": "blue",
    "E": "orange"
}

# Find the book at position 1 (leftmost) and print corresponding letter
for solution in solutions:
    for book_name, position in solution.items():
        if position == 1:
            # Find the choice letter corresponding to this book
            for letter, choice_book in choices.items():
                if choice_book == book_name:
                    print(letter)
            break