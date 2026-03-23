from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
books = ["blue", "orange", "green"]
positions = range(1, 4)
problem.addVariables(books, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The green book is the leftmost"
problem.addConstraint(lambda green: green == 1, ["green"])

# "The orange book is to the left of the blue book"
problem.addConstraint(lambda orange, blue: orange < blue, ["orange", "blue"])

# Solve the problem
solutions = problem.getSolutions()

# Determine which book is rightmost (position 3)
for solution in solutions:
    if solution["blue"] == 3:
        print("A")
    elif solution["orange"] == 3:
        print("B")
    elif solution["green"] == 3:
        print("C")