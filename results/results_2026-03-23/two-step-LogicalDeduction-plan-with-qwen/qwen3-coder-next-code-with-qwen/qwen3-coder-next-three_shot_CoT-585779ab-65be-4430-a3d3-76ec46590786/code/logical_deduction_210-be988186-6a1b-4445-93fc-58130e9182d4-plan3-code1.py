from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (books) and domain (positions 1 to 7)
books = ["black", "yellow", "white", "gray", "purple", "orange", "green"]
positions = range(1, 8)
problem.addVariables(books, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem statements
# "The green book is to the left of the gray book" → green < gray
problem.addConstraint(lambda green, gray: green < gray, ("green", "gray"))

# "The gray book is the third from the right" → position 5 (since 7-2=5)
problem.addConstraint(lambda gray: gray == 5, ("gray",))

# "The white book is the rightmost" → position 7
problem.addConstraint(lambda white: white == 7, ("white",))

# "The orange book is the second from the left" → position 2
problem.addConstraint(lambda orange: orange == 2, ("orange",))

# "The black book is to the right of the yellow book" → black > yellow
problem.addConstraint(lambda yellow, black: yellow < black, ("yellow", "black"))

# "The black book is the third from the left" → position 3
problem.addConstraint(lambda black: black == 3, ("black",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to book names
choices = {
    "A": "black",
    "B": "yellow",
    "C": "white",
    "D": "gray",
    "E": "purple",
    "F": "orange",
    "G": "green"
}

# Find which book is at position 7 (rightmost)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 7:
            print(letter)