from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (books) and domain (positions 1 to 5, where 1 is leftmost)
books = ["green", "blue", "brown", "gray", "red"]
positions = range(1, 6)
problem.addVariables(books, positions)

# Add constraints based on the problem statements
# 1. All books must be in different positions
problem.addConstraint(AllDifferentConstraint())

# 2. "The green book is to the left of the brown book" → green < brown
problem.addConstraint(lambda green, brown: green < brown, ["green", "brown"])

# 3. "The gray book is to the left of the blue book" → gray < blue
problem.addConstraint(lambda gray, blue: gray < blue, ["gray", "blue"])

# 4. "The green book is to the right of the blue book" → green > blue
problem.addConstraint(lambda green, blue: green > blue, ["green", "blue"])

# 5. "The red book is the leftmost" → red == 1
problem.addConstraint(lambda red: red == 1, ["red"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to book names for the question about third from left (position 3)
choices = {
    "A": "green",
    "B": "blue",
    "C": "brown",
    "D": "gray",
    "E": "red"
}

# Find which book is at position 3 and print the corresponding choice letter
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 3:
            print(letter)