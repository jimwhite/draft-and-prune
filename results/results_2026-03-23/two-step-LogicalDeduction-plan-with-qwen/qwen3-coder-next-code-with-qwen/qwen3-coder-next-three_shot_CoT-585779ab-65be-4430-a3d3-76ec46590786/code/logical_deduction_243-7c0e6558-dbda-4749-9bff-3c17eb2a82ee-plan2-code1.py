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

# Solve for the arrangement
solutions = problem.getSolutions()

# Determine which book is rightmost (position 3)
for solution in solutions:
    if solution["red"] == 3:
        print("A")
    elif solution["gray"] == 3:
        print("B")
    elif solution["white"] == 3:
        print("C")