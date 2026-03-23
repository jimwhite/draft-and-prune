from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
books = ["red", "gray", "white"]
positions = range(1, 4)
problem.addVariables(books, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The white book is to the left of the gray book"
problem.addConstraint(lambda white, gray: white < gray, ("white", "gray"))

# "The red book is the second from the left"
problem.addConstraint(lambda red: red == 2, ("red",))

# Solve the problem
solutions = problem.getSolutions()

# Determine the correct answer
for solution in solutions:
    if solution["red"] == 2:
        print("A")