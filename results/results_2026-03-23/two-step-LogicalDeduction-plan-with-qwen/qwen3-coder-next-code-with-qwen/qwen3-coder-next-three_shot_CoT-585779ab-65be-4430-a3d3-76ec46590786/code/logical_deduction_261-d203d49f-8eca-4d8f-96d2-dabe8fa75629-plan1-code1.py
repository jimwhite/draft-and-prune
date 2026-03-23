from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
books = ["purple", "black", "blue"]
positions = range(1, 4)
problem.addVariables(books, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The purple book is to the right of the blue book"
problem.addConstraint(lambda purple, blue: purple > blue, ["purple", "blue"])

# "The black book is the second from the left"
problem.addConstraint(lambda black: black == 2, ["black"])

# Solve the problem
solutions = problem.getSolutions()

# Evaluate choices
choices = {
    "A": ("purple", 2),
    "B": ("black", 2),
    "C": ("blue", 2)
}

# Find which choice is true
for solution in solutions:
    for letter, (book_name, position) in choices.items():
        if solution[book_name] == position:
            print(letter)