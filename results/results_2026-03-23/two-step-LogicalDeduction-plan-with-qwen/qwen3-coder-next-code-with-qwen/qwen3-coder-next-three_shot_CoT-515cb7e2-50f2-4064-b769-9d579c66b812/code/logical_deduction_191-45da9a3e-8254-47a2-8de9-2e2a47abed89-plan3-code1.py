from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (books) and domain (positions 1 to 7)
books = ["orange", "red", "green", "white", "purple", "brown", "yellow"]
positions = range(1, 8)
problem.addVariables(books, positions)

# Add AllDifferentConstraint to ensure each book is in a unique position
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# 1. "The green book is to the left of the purple book" → green < purple
problem.addConstraint(lambda g, p: g < p, ["green", "purple"])

# 2. "The white book is to the right of the orange book" → orange < white
problem.addConstraint(lambda o, w: o < w, ["orange", "white"])

# 3. "The green book is to the right of the brown book" → brown < green
problem.addConstraint(lambda b, g: b < g, ["brown", "green"])

# 4. "The yellow book is to the right of the white book" → white < yellow
problem.addConstraint(lambda w, y: w < y, ["white", "yellow"])

# 5. "The red book is to the right of the yellow book" → yellow < red
problem.addConstraint(lambda y, r: y < r, ["yellow", "red"])

# 6. "The brown book is to the right of the red book" → red < brown
problem.addConstraint(lambda r, b: r < b, ["red", "brown"])

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

# Find which book is at position 2 (second from the left)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 2:
            print(letter)