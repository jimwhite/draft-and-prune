from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
books = ["yellow", "green", "red"]
positions = range(1, 4)
problem.addVariables(books, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The red book is to the left of the green book"
problem.addConstraint(lambda red, green: red < green, ("red", "green"))

# "The yellow book is to the left of the red book"
problem.addConstraint(lambda yellow, red: yellow < red, ("yellow", "red"))

# Solve the problem
solutions = problem.getSolutions()

# Determine which book is second from the left (position 2)
for solution in solutions:
    if solution["yellow"] == 2:
        print("A")
    elif solution["green"] == 2:
        print("B")
    elif solution["red"] == 2:
        print("C")