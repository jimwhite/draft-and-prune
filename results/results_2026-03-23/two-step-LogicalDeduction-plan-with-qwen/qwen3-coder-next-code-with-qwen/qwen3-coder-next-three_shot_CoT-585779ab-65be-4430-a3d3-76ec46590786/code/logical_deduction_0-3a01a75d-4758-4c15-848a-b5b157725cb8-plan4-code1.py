from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables (books) and domain (positions 1 to 5, where 1 is leftmost)
books = ["green", "blue", "white", "purple", "yellow"]
positions = range(1, 6)
problem.addVariables(books, positions)

# Add constraints
# All books must be in different positions
problem.addConstraint(AllDifferentConstraint())

# "The blue book is to the right of the yellow book" → blue > yellow
problem.addConstraint(lambda blue, yellow: blue > yellow, ("blue", "yellow"))

# "The white book is to the left of the yellow book" → white < yellow
problem.addConstraint(lambda white, yellow: white < yellow, ("white", "yellow"))

# "The blue book is the second from the right" → blue == 4
problem.addConstraint(lambda blue: blue == 4, ("blue",))

# "The purple book is the second from the left" → purple == 2
problem.addConstraint(lambda purple: purple == 2, ("purple",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to books mentioned in each option (the book claimed to be second from left)
choices = {
    "A": "green",
    "B": "blue",
    "C": "white",
    "D": "purple",
    "E": "yellow"
}

# Find which book is at position 2 (second from left) and print the corresponding choice letter
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 2:
            print(letter)