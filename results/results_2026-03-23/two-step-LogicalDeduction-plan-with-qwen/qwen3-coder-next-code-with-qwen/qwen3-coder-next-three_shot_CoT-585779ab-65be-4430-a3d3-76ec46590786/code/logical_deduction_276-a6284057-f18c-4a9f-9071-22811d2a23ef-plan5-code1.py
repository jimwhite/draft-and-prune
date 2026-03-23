from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (the three books) and domain (positions 1 to 3)
books = ["purple", "red", "yellow"]
positions = range(1, 4)
problem.addVariables(books, positions)

# Add constraints based on the statements
# All books must be in different positions
problem.addConstraint(AllDifferentConstraint())

# "The purple book is to the right of the yellow book" => purple > yellow
problem.addConstraint(lambda purple, yellow: purple > yellow, ("purple", "yellow"))

# "The yellow book is to the right of the red book" => yellow > red
problem.addConstraint(lambda yellow, red: yellow > red, ("yellow", "red"))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to book names
choices = {
    "A": "purple",
    "B": "red",
    "C": "yellow"
}

# Find the leftmost book (position 1) and print the corresponding choice letter
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 1:
            print(letter)