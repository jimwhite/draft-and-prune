from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables (books) and domain (positions 1 to 5, where 1 is leftmost)
books = ["brown", "orange", "red", "purple", "black"]
positions = range(1, 6)
problem.addVariables(books, positions)

# Add constraints based on the problem statements
# 1. All books must be in different positions
problem.addConstraint(AllDifferentConstraint())

# 2. "The purple book is to the left of the black book"
problem.addConstraint(lambda purple, black: purple < black, ("purple", "black"))

# 3. "The red book is to the right of the brown book"
problem.addConstraint(lambda brown, red: brown < red, ("brown", "red"))

# 4. "The orange book is the second from the left"
problem.addConstraint(lambda orange: orange == 2, ("orange",))

# 5. "The black book is the third from the left"
problem.addConstraint(lambda black: black == 3, ("black",))

# Solve for the arrangement
solutions = problem.getSolutions()

# The question asks which book is the second from the left (position 2)
# According to choice B: "The orange book is the second from the left."
# Since we have a constraint that orange == 2, the answer is B
for solution in solutions:
    if solution["orange"] == 2:
        print("B")