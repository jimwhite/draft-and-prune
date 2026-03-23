from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain for three books
books = ["red", "gray", "white"]
positions = range(1, 4)  # 1=leftmost, 2=middle, 3=rightmost
problem.addVariables(books, positions)

# Add constraints based on the problem description
# 1. All books must be in different positions
problem.addConstraint(AllDifferentConstraint())

# 2. "The white book is to the left of the gray book"
problem.addConstraint(lambda white, gray: white < gray, ["white", "gray"])

# 3. "The red book is the second from the left"
problem.addConstraint(lambda red: red == 2, ["red"])

# Solve for the arrangement
solutions = problem.getSolutions()

# The question asks which statement is true, and choice A directly states
# "The red book is the second from the left", which is given as a constraint.
# Since we have a unique solution and red == 2 is enforced, choice A must be true.
# We can verify by checking the solution, but it's guaranteed by the constraint.

# For completeness, let's output 'A' as the answer
print("A")