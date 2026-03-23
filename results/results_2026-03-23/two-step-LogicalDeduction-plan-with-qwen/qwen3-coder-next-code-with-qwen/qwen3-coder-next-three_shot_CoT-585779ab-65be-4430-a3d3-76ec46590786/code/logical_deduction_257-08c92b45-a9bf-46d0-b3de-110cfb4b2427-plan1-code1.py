from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
books = ["yellow", "green", "red"]
positions = range(1, 4)
problem.addVariables(books, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# The red book is to the left of the green book: red < green
problem.addConstraint(lambda r, g: r < g, ("red", "green"))

# The yellow book is to the left of the red book: yellow < red
problem.addConstraint(lambda y, r: y < r, ("yellow", "red"))

# Solve for all valid arrangements
solutions = problem.getSolutions()

# Determine the correct answer (second from the left means position 2)
for solution in solutions:
    if solution["yellow"] == 2:
        print("A")
    elif solution["green"] == 2:
        print("B")
    elif solution["red"] == 2:
        print("C")