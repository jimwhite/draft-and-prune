from constraint import *

# Set up the problem
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

# Solve
solutions = problem.getSolutions()

# Determine the correct answer by checking which book is at position 2
for solution in solutions:
    if solution["black"] == 2:
        print("B")