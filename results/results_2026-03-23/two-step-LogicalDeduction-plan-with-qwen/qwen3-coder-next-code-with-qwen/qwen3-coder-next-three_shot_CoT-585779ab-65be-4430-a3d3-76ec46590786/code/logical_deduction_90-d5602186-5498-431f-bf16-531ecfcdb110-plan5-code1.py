from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (books) and domain (positions 1 to 5, where 1=leftmost, 5=rightmost)
books = ["green", "orange", "gray", "yellow", "purple"]
positions = range(1, 6)
problem.addVariables(books, positions)

# Add constraints
# All books must be in different positions
problem.addConstraint(AllDifferentConstraint())

# "The green book is the rightmost" → green == 5
problem.addConstraint(lambda green: green == 5, ["green"])

# "The gray book is to the right of the orange book" → orange < gray
problem.addConstraint(lambda orange, gray: orange < gray, ["orange", "gray"])

# "The purple book is to the left of the yellow book" → purple < yellow
problem.addConstraint(lambda purple, yellow: purple < yellow, ["purple", "yellow"])

# "The purple book is to the right of the gray book" → gray < purple
problem.addConstraint(lambda gray, purple: gray < purple, ["gray", "purple"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to book names for the question about "third from the left" (position 3)
choices = {
    "A": "green",
    "B": "orange",
    "C": "gray",
    "D": "yellow",
    "E": "purple"
}

# Find which book is at position 3 and print the corresponding choice letter
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 3:
            print(letter)