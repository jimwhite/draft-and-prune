from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define the seven books as variables
books = ["orange", "green", "red", "gray", "purple", "blue", "brown"]

# Define the domain: positions 1 to 7 (1 = leftmost, 7 = rightmost)
positions = range(1, 8)
problem.addVariables(books, positions)

# Add constraints based on the problem description
# 1. All books must be in different positions
problem.addConstraint(AllDifferentConstraint())

# 2. "The purple book is the fourth from the left."
problem.addConstraint(lambda purple: purple == 4, ["purple"])

# 3. "The brown book is the third from the left."
problem.addConstraint(lambda brown: brown == 3, ["brown"])

# 4. "The green book is to the left of the blue book."
problem.addConstraint(lambda green, blue: green < blue, ["green", "blue"])

# 5. "The red book is the leftmost."
problem.addConstraint(lambda red: red == 1, ["red"])

# 6. "The gray book is the third from the right."
# For 7 positions, third from the right is position 5 (since 7-3+1=5)
problem.addConstraint(lambda gray: gray == 5, ["gray"])

# 7. "The orange book is the rightmost."
problem.addConstraint(lambda orange: orange == 7, ["orange"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to book names
choices = {
    'A': "orange",
    'B': "green",
    'C': "red",
    'D': "gray",
    'E': "purple",
    'F': "blue",
    'G': "brown"
}

# Find which book is at position 4 (fourth from the left)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 4:
            print(letter)