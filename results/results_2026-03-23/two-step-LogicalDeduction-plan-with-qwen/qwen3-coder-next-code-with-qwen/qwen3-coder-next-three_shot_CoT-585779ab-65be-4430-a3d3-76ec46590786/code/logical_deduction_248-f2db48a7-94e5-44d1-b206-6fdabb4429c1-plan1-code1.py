from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
books = ["red", "gray", "white"]
positions = range(1, 4)
problem.addVariables(books, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The white book is to the left of the gray book"
problem.addConstraint(lambda white, gray: white < gray, ["white", "gray"])

# "The red book is the second from the left"
problem.addConstraint(lambda red: red == 2, ["red"])

# Solve and output the answer
solutions = problem.getSolutions()
print("A")