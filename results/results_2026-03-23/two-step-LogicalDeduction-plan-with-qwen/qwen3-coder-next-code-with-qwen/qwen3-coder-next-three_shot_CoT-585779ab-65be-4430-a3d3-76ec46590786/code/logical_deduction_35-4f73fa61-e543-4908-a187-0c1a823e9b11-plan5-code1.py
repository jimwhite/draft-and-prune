from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (books) and domain (positions 1 to 5, left to right)
books = ["white", "orange", "yellow", "blue", "red"]
positions = range(1, 6)
problem.addVariables(books, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# "The yellow book is to the left of the white book" → yellow < white
problem.addConstraint(lambda y, w: y < w, ("yellow", "white"))

# "The red book is to the right of the blue book" → blue < red
problem.addConstraint(lambda b, r: b < r, ("blue", "red"))

# "The yellow book is to the right of the orange book" → orange < yellow
problem.addConstraint(lambda o, y: o < y, ("orange", "yellow"))

# "The blue book is to the right of the white book" → white < blue
problem.addConstraint(lambda w, b: w < b, ("white", "blue"))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to book names
choices = {
    "A": "white",
    "B": "orange",
    "C": "yellow",
    "D": "blue",
    "E": "red"
}

# Find which book is at position 4 (second from the right)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 4:
            print(letter)