from constraint import *

# Initialize the problem environment
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

# Solve for arrangements
solutions = problem.getSolutions()

# Check which choice is true based on the solution
for solution in solutions:
    # Choice A: purple book is second from left (position 2)
    choice_a = solution["purple"] == 2
    # Choice B: black book is second from left (position 2)
    choice_b = solution["black"] == 2
    # Choice C: blue book is second from left (position 2)
    choice_c = solution["blue"] == 2
    
    # Since the constraint ensures black == 2, choice B must be true
    if choice_b:
        print("B")