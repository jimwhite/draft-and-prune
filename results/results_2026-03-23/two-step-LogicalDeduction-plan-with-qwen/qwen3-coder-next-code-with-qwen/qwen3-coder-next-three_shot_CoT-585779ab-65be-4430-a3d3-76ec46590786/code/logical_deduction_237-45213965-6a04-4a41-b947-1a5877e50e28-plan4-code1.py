from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (books) and domain (positions 1 to 7, left to right)
books = ["red", "white", "purple", "black", "gray", "orange", "blue"]
positions = range(1, 8)
problem.addVariables(books, positions)

# Add AllDifferentConstraint to ensure each book is in a unique position
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# 1. "The red book is to the right of the white book" → red > white
problem.addConstraint(lambda red, white: red > white, ("red", "white"))

# 2. "The gray book is to the left of the orange book" → gray < orange
problem.addConstraint(lambda gray, orange: gray < orange, ("gray", "orange"))

# 3. "The gray book is to the right of the blue book" → gray > blue
problem.addConstraint(lambda gray, blue: gray > blue, ("gray", "blue"))

# 4. "The red book is the second from the right" → red == 6
problem.addConstraint(lambda red: red == 6, ("red",))

# 5. "The black book is the fourth from the left" → black == 4
problem.addConstraint(lambda black: black == 4, ("black",))

# 6. "The orange book is to the left of the white book" → orange < white
problem.addConstraint(lambda orange, white: orange < white, ("orange", "white"))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to book names
choices = {
    "A": "red",
    "B": "white",
    "C": "purple",
    "D": "black",
    "E": "gray",
    "F": "orange",
    "G": "blue"
}

# Find the book at position 5 (third from the right in a 7-position shelf)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 5:
            print(letter)