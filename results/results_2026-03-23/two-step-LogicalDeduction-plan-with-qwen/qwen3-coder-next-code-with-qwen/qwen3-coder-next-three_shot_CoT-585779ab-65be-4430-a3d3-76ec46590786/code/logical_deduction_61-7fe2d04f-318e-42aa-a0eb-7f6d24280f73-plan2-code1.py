from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
books = ["gray", "red", "purple", "blue", "black"]
positions = range(1, 6)
problem.addVariables(books, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The red book is to the right of the gray book" -> gray < red
problem.addConstraint(lambda gray, red: gray < red, ("gray", "red"))

# "The black book is to the left of the blue book" -> black < blue
problem.addConstraint(lambda black, blue: black < blue, ("black", "blue"))

# "The blue book is to the left of the gray book" -> blue < gray
problem.addConstraint(lambda blue, gray: blue < gray, ("blue", "gray"))

# "The purple book is the second from the right" -> position 4
problem.addConstraint(lambda purple: purple == 4, ("purple",))

# Solve the problem
solutions = problem.getSolutions()

# Since we know from the constraint that purple must be at position 4,
# and the problem states the statements are consistent, we can directly
# output 'C' as the correct answer (Choice C states "The purple book is the second from the right.")
print("C")