from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (books) and domain (positions 1 to 5, where 1 is leftmost)
books = ["green", "blue", "brown", "gray", "red"]
positions = range(1, 6)
problem.addVariables(books, positions)

# Add AllDifferent constraint to ensure each book is in a unique position
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "The green book is to the left of the brown book" → green < brown
problem.addConstraint(lambda green, brown: green < brown, ["green", "brown"])

# "The gray book is to the left of the blue book" → gray < blue
problem.addConstraint(lambda gray, blue: gray < blue, ["gray", "blue"])

# "The green book is to the right of the blue book" → green > blue
problem.addConstraint(lambda green, blue: green > blue, ["green", "blue"])

# "The red book is the leftmost" → red == 1
problem.addConstraint(lambda red: red == 1, ["red"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to book names (second from right means position 4)
choices = {
    "A": "green",
    "B": "blue",
    "C": "brown",
    "D": "gray",
    "E": "red"
}

# Find which book is at position 4 (second from right) and print the corresponding letter
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 4:
            print(letter)