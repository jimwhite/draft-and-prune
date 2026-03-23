from constraint import *

# Initialize the problem
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

# Check which choice is true based on the solution
for solution in solutions:
    # Choice A: purple == 2 (but black must be 2, so this is false)
    # Choice B: black == 2 (this matches our constraint, so it's true)
    # Choice C: blue == 2 (but black must be 2, so this is false)
    # Since we know black == 2 from the constraint, choice B must be true
    print("B")