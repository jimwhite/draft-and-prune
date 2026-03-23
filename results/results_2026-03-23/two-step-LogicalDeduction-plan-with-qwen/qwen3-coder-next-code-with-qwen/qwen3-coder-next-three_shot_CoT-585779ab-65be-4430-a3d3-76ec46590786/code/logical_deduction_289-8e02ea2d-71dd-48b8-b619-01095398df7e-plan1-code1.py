from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
books = ["purple", "white", "blue"]
positions = range(1, 4)
problem.addVariables(books, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The purple book is to the left of the blue book" -> purple < blue
problem.addConstraint(lambda purple, blue: purple < blue, ["purple", "blue"])

# "The purple book is to the right of the white book" -> white < purple
problem.addConstraint(lambda white, purple: white < purple, ["white", "purple"])

# Solve the problem
solutions = problem.getSolutions()

# Determine which book is in position 2 (second from the left)
for solution in solutions:
    if solution["purple"] == 2:
        print("A")
    elif solution["white"] == 2:
        print("B")
    elif solution["blue"] == 2:
        print("C")