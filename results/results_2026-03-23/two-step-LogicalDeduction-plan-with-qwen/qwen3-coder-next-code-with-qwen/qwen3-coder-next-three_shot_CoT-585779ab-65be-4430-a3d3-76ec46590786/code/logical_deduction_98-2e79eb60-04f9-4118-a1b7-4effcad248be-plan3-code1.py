from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
books = ["yellow", "gray", "red", "black", "white"]
positions = range(1, 6)
problem.addVariables(books, positions)

# Add all different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# "The gray book is to the left of the yellow book"
problem.addConstraint(lambda gray, yellow: gray < yellow, ("gray", "yellow"))

# "The white book is to the left of the red book"
problem.addConstraint(lambda white, red: white < red, ("white", "red"))

# "The black book is to the right of the red book"
problem.addConstraint(lambda red, black: red < black, ("red", "black"))

# "The black book is to the left of the gray book"
problem.addConstraint(lambda black, gray: black < gray, ("black", "gray"))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to book names
choices = {
    "A": "yellow",
    "B": "gray",
    "C": "red",
    "D": "black",
    "E": "white"
}

# Find which book is at position 3 (third from the left)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 3:
            print(letter)