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
# "The green book is to the left of the purple book"
problem.addConstraint(lambda g, p: g < p, ("green", "purple"))

# "The white book is to the right of the orange book"
problem.addConstraint(lambda o, w: o < w, ("orange", "white"))

# "The green book is to the right of the brown book"
problem.addConstraint(lambda b, g: b < g, ("brown", "green"))

# "The yellow book is to the right of the white book"
problem.addConstraint(lambda w, y: w < y, ("white", "yellow"))

# "The red book is to the right of the yellow book"
problem.addConstraint(lambda y, r: y < r, ("yellow", "red"))

# "The brown book is to the right of the red book"
problem.addConstraint(lambda r, b: r < b, ("red", "brown"))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to book names
choices = {
    'A': 'orange',
    'B': 'red',
    'C': 'green',
    'D': 'white',
    'E': 'purple',
    'F': 'brown',
    'G': 'yellow'
}

# Find the book at position 2 (second from left)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 2:
            print(letter)