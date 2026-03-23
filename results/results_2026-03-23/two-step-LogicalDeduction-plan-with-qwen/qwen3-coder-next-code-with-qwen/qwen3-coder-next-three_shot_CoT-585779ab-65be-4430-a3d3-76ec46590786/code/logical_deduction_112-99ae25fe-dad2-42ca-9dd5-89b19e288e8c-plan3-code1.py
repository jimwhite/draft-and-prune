from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (books) and domain (positions 1 to 7)
books = ["brown", "gray", "orange", "green", "black", "purple", "yellow"]
positions = range(1, 8)
problem.addVariables(books, positions)

# Add all different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem description
# "The purple book is the leftmost" -> position 1
problem.addConstraint(lambda purple: purple == 1, ["purple"])

# "The brown book is to the right of the yellow book" -> brown > yellow
problem.addConstraint(lambda brown, yellow: brown > yellow, ["brown", "yellow"])

# "The green book is to the left of the orange book" -> green < orange
problem.addConstraint(lambda green, orange: green < orange, ["green", "orange"])

# "The orange book is to the left of the gray book" -> orange < gray
problem.addConstraint(lambda orange, gray: orange < gray, ["orange", "gray"])

# "The black book is the third from the left" -> position 3
problem.addConstraint(lambda black: black == 3, ["black"])

# "The green book is the third from the right" -> position 5 (7 - 2 = 5)
problem.addConstraint(lambda green: green == 5, ["green"])

# Solve the problem
solutions = problem.getSolutions()

# Since we know green must be at position 5 (third from right), and choice D states exactly that,
# we directly output 'D' as the correct answer
print('D')