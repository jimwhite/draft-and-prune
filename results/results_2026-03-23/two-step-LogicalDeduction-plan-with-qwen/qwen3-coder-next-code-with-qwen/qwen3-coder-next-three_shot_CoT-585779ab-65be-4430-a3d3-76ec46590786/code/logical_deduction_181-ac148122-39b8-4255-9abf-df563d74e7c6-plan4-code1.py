from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (the seven books) and domain (positions 1 to 7)
books = ["orange", "red", "brown", "blue", "black", "gray", "white"]
positions = range(1, 8)
problem.addVariables(books, positions)

# Add constraints based on the problem description
# 1. All books must be in different positions
problem.addConstraint(AllDifferentConstraint())

# 2. "The white book is the leftmost."
problem.addConstraint(lambda white: white == 1, ["white"])

# 3. "The red book is to the right of the blue book."
problem.addConstraint(lambda blue, red: blue < red, ["blue", "red"])

# 4. "The orange book is the second from the right."
problem.addConstraint(lambda orange: orange == 6, ["orange"])

# 5. "The gray book is the fourth from the left."
problem.addConstraint(lambda gray: gray == 4, ["gray"])

# 6. "The black book is the rightmost."
problem.addConstraint(lambda black: black == 7, ["black"])

# 7. "The gray book is to the right of the red book."
problem.addConstraint(lambda red, gray: red < gray, ["red", "gray"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to book names
choices = {
    "A": "orange",
    "B": "red",
    "C": "brown",
    "D": "blue",
    "E": "black",
    "F": "gray",
    "G": "white"
}

# Find the book at position 2 (second from left)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 2:
            print(letter)