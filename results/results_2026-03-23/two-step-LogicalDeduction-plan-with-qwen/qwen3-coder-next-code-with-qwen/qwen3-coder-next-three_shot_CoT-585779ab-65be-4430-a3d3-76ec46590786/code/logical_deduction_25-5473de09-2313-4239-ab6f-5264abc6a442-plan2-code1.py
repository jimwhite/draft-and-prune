from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (books) and domain (positions 1 to 5, where 1=leftmost, 5=rightmost)
books = ["blue", "purple", "yellow", "black", "green"]
positions = range(1, 6)
problem.addVariables(books, positions)

# Add constraints
# All books must be in different positions
problem.addConstraint(AllDifferentConstraint())

# The purple book is the third from the left (position 3)
problem.addConstraint(lambda purple: purple == 3, ["purple"])

# The yellow book is to the left of the black book (yellow < black)
problem.addConstraint(lambda yellow, black: yellow < black, ["yellow", "black"])

# The green book is to the left of the purple book (green < 3)
problem.addConstraint(lambda green: green < 3, ["green"])

# The blue book is to the left of the green book (blue < green)
problem.addConstraint(lambda blue, green: blue < green, ["blue", "green"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to book names
choices = {
    "A": "blue",
    "B": "purple",
    "C": "yellow",
    "D": "black",
    "E": "green"
}

# Find which book is at position 4 (second from the right)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 4:
            print(letter)