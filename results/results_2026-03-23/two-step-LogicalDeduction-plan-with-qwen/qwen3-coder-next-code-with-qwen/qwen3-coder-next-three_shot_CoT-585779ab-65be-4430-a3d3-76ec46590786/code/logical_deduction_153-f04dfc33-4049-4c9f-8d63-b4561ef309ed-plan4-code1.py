from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (books) and domain (positions 1 to 7, where 1=leftmost, 7=rightmost)
books = ["yellow", "red", "gray", "blue", "white", "orange", "purple"]
positions = range(1, 8)
problem.addVariables(books, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem statements:
# 1. "The red book is the third from the right" → position 5 (7 - 2 = 5)
problem.addConstraint(lambda red: red == 5, ["red"])

# 2. "The white book is to the right of the orange book" → orange < white
problem.addConstraint(lambda orange, white: orange < white, ["orange", "white"])

# 3. "The purple book is the third from the left" → position 3
problem.addConstraint(lambda purple: purple == 3, ["purple"])

# 4. "The yellow book is to the right of the purple book" → purple < yellow
problem.addConstraint(lambda purple, yellow: purple < yellow, ["purple", "yellow"])

# 5. "The blue book is to the right of the red book" → red < blue
problem.addConstraint(lambda red, blue: red < blue, ["red", "blue"])

# 6. "The blue book is to the left of the gray book" → blue < gray
problem.addConstraint(lambda blue, gray: blue < gray, ["blue", "gray"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to book names
choices = {
    "A": "yellow",
    "B": "red",
    "C": "gray",
    "D": "blue",
    "E": "white",
    "F": "orange",
    "G": "purple"
}

# Find which book is at position 2 (second from the left)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 2:
            print(letter)