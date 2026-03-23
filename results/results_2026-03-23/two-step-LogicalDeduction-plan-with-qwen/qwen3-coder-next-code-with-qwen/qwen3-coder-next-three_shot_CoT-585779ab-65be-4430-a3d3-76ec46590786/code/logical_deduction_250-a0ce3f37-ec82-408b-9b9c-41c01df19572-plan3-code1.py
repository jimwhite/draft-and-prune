from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
books = ["white", "black", "purple"]
positions = range(1, 4)
problem.addVariables(books, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The black book is to the left of the purple book"
problem.addConstraint(lambda black, purple: black < purple, ["black", "purple"])

# "The purple book is to the left of the white book"
problem.addConstraint(lambda purple, white: purple < white, ["purple", "white"])

# Solve the problem
solutions = problem.getSolutions()

# Determine which book is rightmost (position 3)
for solution in solutions:
    if solution["white"] == 3:
        print("A")