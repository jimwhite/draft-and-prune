from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
books = ["black", "brown", "yellow", "orange", "red"]
positions = range(1, 6)
problem.addVariables(books, positions)

# Add all different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# "The black book is to the left of the yellow book"
problem.addConstraint(lambda black, yellow: black < yellow, ["black", "yellow"])

# "The red book is the third from the left"
problem.addConstraint(lambda red: red == 3, ["red"])

# "The brown book is the second from the left"
problem.addConstraint(lambda brown: brown == 2, ["brown"])

# "The yellow book is to the left of the orange book"
problem.addConstraint(lambda yellow, orange: yellow < orange, ["yellow", "orange"])

# Solve the problem
solutions = problem.getSolutions()

# Determine which book is rightmost (position 5)
for solution in solutions:
    if solution["black"] == 5:
        print("A")
    elif solution["brown"] == 5:
        print("B")
    elif solution["yellow"] == 5:
        print("C")
    elif solution["orange"] == 5:
        print("D")
    elif solution["red"] == 5:
        print("E")