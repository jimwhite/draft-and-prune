from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (books) and domain (positions 1 to 7)
books = ["red", "purple", "green", "white", "orange", "blue", "gray"]
positions = range(1, 8)
problem.addVariables(books, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem statements
# Green book is to the left of white book: green < white
problem.addConstraint(lambda green, white: green < white, ("green", "white"))

# Red book is to the left of purple book: red < purple
problem.addConstraint(lambda red, purple: red < purple, ("red", "purple"))

# Red book is to the right of orange book: orange < red
problem.addConstraint(lambda orange, red: orange < red, ("orange", "red"))

# Gray book is the second from the left: gray == 2
problem.addConstraint(lambda gray: gray == 2, ("gray",))

# Purple book is to the left of green book: purple < green
problem.addConstraint(lambda purple, green: purple < green, ("purple", "green"))

# Blue book is the fourth from the left: blue == 4
problem.addConstraint(lambda blue: blue == 4, ("blue",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to book names
choices = {
    "A": "red",
    "B": "purple",
    "C": "green",
    "D": "white",
    "E": "orange",
    "F": "blue",
    "G": "gray"
}

# Find which book is at position 2 (second from the left)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 2:
            print(letter)