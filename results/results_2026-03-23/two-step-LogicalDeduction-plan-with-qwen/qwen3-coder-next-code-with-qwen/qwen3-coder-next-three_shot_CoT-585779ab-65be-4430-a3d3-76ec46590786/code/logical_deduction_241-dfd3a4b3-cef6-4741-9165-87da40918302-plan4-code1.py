from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables and domain for three books
books = ["gray", "purple", "red"]
positions = range(1, 4)  # 1=leftmost, 2=middle, 3=rightmost
problem.addVariables(books, positions)

# Add constraints based on the statements
# All books must be in different positions
problem.addConstraint(AllDifferentConstraint())

# "The purple book is to the left of the red book" -> purple < red
problem.addConstraint(lambda purple, red: purple < red, ["purple", "red"])

# "The gray book is to the left of the purple book" -> gray < purple
problem.addConstraint(lambda gray, purple: gray < purple, ["gray", "purple"])

# Solve for the arrangement
solutions = problem.getSolutions()

# Determine which book is in position 2 (second from the left)
for solution in solutions:
    if solution["gray"] == 2:
        print("A")
    elif solution["purple"] == 2:
        print("B")
    elif solution["red"] == 2:
        print("C")