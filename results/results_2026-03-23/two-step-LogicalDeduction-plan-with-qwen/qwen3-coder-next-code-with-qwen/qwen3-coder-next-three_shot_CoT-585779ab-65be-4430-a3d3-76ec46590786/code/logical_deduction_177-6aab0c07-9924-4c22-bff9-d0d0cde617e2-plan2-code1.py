from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (books) and domain (positions 1 to 7)
books = ["orange", "green", "red", "gray", "purple", "blue", "brown"]
positions = range(1, 8)
problem.addVariables(books, positions)

# Add all different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem description
# "The purple book is the fourth from the left"
problem.addConstraint(lambda purple: purple == 4, ["purple"])

# "The brown book is the third from the left"
problem.addConstraint(lambda brown: brown == 3, ["brown"])

# "The green book is to the left of the blue book"
problem.addConstraint(lambda green, blue: green < blue, ["green", "blue"])

# "The red book is the leftmost"
problem.addConstraint(lambda red: red == 1, ["red"])

# "The gray book is the third from the right" (position 5 in a 7-position sequence)
problem.addConstraint(lambda gray: gray == 5, ["gray"])

# "The orange book is the rightmost"
problem.addConstraint(lambda orange: orange == 7, ["orange"])

# Solve the problem
solutions = problem.getSolutions()

# Determine which book is third from the right (position 5)
# According to constraints, gray must be at position 5
# So choice D is correct: "The gray book is the third from the right."

# Check which book is at position 5
solution = solutions[0]
for letter, book in [("A", "orange"), ("B", "green"), ("C", "red"), 
                      ("D", "gray"), ("E", "purple"), ("F", "blue"), ("G", "brown")]:
    if solution[book] == 5:
        print(letter)