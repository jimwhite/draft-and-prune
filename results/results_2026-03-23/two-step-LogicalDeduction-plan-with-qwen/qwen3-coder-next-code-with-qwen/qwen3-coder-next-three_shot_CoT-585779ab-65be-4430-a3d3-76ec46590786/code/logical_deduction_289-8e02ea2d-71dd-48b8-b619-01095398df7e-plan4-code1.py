from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables and domain
books = ["purple", "white", "blue"]
positions = range(1, 4)
problem.addVariables(books, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The purple book is to the left of the blue book" => purple < blue
problem.addConstraint(lambda purple, blue: purple < blue, ("purple", "blue"))

# "The purple book is to the right of the white book" => white < purple
problem.addConstraint(lambda white, purple: white < purple, ("white", "purple"))

# Solve for the arrangement
solutions = problem.getSolutions()

# Map choice letters to book names
choices = {
    "A": "purple",
    "B": "white",
    "C": "blue"
}

# Find which book is in position 2 (second from the left)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 2:
            print(letter)