from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (the three books) and domain (positions 1 to 3)
books = ["gray", "orange", "brown"]
positions = range(1, 4)
problem.addVariables(books, positions)

# Add constraints
# All books must be in different positions
problem.addConstraint(AllDifferentConstraint())

# "The orange book is the leftmost" -> orange == 1
problem.addConstraint(lambda orange: orange == 1, ["orange"])

# "The gray book is to the right of the brown book" -> brown < gray
problem.addConstraint(lambda brown, gray: brown < gray, ["brown", "gray"])

# Solve the problem
solutions = problem.getSolutions()

# Determine which book is rightmost (position 3)
for solution in solutions:
    if solution["gray"] == 3:
        print("A")
    elif solution["orange"] == 3:
        print("B")
    elif solution["brown"] == 3:
        print("C")