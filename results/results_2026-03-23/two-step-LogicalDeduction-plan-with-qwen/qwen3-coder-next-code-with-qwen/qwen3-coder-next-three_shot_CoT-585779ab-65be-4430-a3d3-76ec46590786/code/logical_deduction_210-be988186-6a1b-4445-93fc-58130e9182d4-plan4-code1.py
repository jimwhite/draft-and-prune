from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (books) and domain (positions 1 to 7)
books = ["black", "yellow", "white", "gray", "purple", "orange", "green"]
positions = range(1, 8)
problem.addVariables(books, positions)

# Add all different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem description
# "The green book is to the left of the gray book" → green < gray
problem.addConstraint(lambda green, gray: green < gray, ("green", "gray"))

# "The gray book is the third from the right" → gray == 5
problem.addConstraint(lambda gray: gray == 5, ("gray",))

# "The white book is the rightmost" → white == 7
problem.addConstraint(lambda white: white == 7, ("white",))

# "The orange book is the second from the left" → orange == 2
problem.addConstraint(lambda orange: orange == 2, ("orange",))

# "The black book is to the right of the yellow book" → yellow < black
problem.addConstraint(lambda yellow, black: yellow < black, ("yellow", "black"))

# "The black book is the third from the left" → black == 3
problem.addConstraint(lambda black: black == 3, ("black",))

# Solve the problem
solutions = problem.getSolutions()

# Find which book is at position 7 (rightmost)
for solution in solutions:
    if solution["white"] == 7:
        print("C")