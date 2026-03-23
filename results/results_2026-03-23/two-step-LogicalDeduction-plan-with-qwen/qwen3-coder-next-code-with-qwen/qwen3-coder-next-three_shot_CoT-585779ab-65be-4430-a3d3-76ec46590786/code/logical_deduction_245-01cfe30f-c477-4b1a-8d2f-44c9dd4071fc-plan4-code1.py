from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (the three books) and domain (positions 1 to 3)
books = ["orange", "yellow", "blue"]
positions = range(1, 4)
problem.addVariables(books, positions)

# Add constraints based on the statements
# All books must be in different positions
problem.addConstraint(AllDifferentConstraint())

# "The blue book is to the right of the yellow book" => yellow < blue
problem.addConstraint(lambda yellow, blue: yellow < blue, ("yellow", "blue"))

# "The orange book is the second from the left" => orange == 2
problem.addConstraint(lambda orange: orange == 2, ("orange",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to book names
choices = {
    "A": "orange",
    "B": "yellow",
    "C": "blue"
}

# Find which book is rightmost (position 3) and print the corresponding choice letter
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 3:
            print(letter)