from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (books) and domain (positions 1 to 5, where 1=leftmost, 5=rightmost)
books = ["yellow", "green", "gray", "blue", "orange"]
positions = range(1, 6)
problem.addVariables(books, positions)

# Add constraints
# All books must be in different positions
problem.addConstraint(AllDifferentConstraint())

# Gray book is to the left of green book: gray < green
problem.addConstraint(lambda gray, green: gray < green, ("gray", "green"))

# Gray book is second from the right: position 4
problem.addConstraint(lambda gray: gray == 4, ("gray",))

# Yellow book is to the right of orange book: orange < yellow
problem.addConstraint(lambda orange, yellow: orange < yellow, ("orange", "yellow"))

# Blue book is second from the left: position 2
problem.addConstraint(lambda blue: blue == 2, ("blue",))

# Solve the problem
solutions = problem.getSolutions()

# Determine which book is rightmost (position 5)
for solution in solutions:
    if solution["yellow"] == 5:
        print("A")
    elif solution["green"] == 5:
        print("B")
    elif solution["gray"] == 5:
        print("C")
    elif solution["blue"] == 5:
        print("D")
    elif solution["orange"] == 5:
        print("E")