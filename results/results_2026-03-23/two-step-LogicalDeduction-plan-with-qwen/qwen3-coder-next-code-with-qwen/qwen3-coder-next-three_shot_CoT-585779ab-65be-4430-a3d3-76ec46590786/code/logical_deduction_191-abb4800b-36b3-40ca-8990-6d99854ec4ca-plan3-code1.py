from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (books) and domain (positions 1 to 7)
books = ["orange", "red", "green", "white", "purple", "brown", "yellow"]
positions = range(1, 8)
problem.addVariables(books, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# "The green book is to the left of the purple book" → green < purple
problem.addConstraint(lambda green, purple: green < purple, ("green", "purple"))

# "The white book is to the right of the orange book" → orange < white
problem.addConstraint(lambda orange, white: orange < white, ("orange", "white"))

# "The green book is to the right of the brown book" → brown < green
problem.addConstraint(lambda brown, green: brown < green, ("brown", "green"))

# "The yellow book is to the right of the white book" → white < yellow
problem.addConstraint(lambda white, yellow: white < yellow, ("white", "yellow"))

# "The red book is to the right of the yellow book" → yellow < red
problem.addConstraint(lambda yellow, red: yellow < red, ("yellow", "red"))

# "The brown book is to the right of the red book" → red < brown
problem.addConstraint(lambda red, brown: red < brown, ("red", "brown"))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to book names
choices = {
    "A": "orange",
    "B": "red",
    "C": "green",
    "D": "white",
    "E": "purple",
    "F": "brown",
    "G": "yellow"
}

# Find which book is in position 2 (second from the left)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 2:
            print(letter)