from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain for three books
books = ["purple", "white", "blue"]
positions = range(1, 4)  # 1=leftmost, 3=rightmost
problem.addVariables(books, positions)

# Add constraints based on the statements
# 1. All books must be in different positions
problem.addConstraint(AllDifferentConstraint())

# 2. "The purple book is to the left of the blue book" => purple < blue
problem.addConstraint(lambda purple, blue: purple < blue, ("purple", "blue"))

# 3. "The purple book is to the right of the white book" => white < purple
problem.addConstraint(lambda white, purple: white < purple, ("white", "purple"))

# Solve for the unique arrangement
solutions = problem.getSolutions()

# Determine which book is rightmost (position 3)
for solution in solutions:
    if solution["purple"] == 3:
        print("A")
    elif solution["white"] == 3:
        print("B")
    elif solution["blue"] == 3:
        print("C")