from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (the seven books) and domain (positions 1 to 7)
books = ["orange", "red", "brown", "blue", "black", "gray", "white"]
positions = range(1, 8)
problem.addVariables(books, positions)

# Add AllDifferent constraint to ensure each book is in a unique position
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem statements:
# 1. "The white book is the leftmost" → position 1
problem.addConstraint(lambda white: white == 1, ["white"])

# 2. "The red book is to the right of the blue book" → blue < red
problem.addConstraint(lambda blue, red: blue < red, ["blue", "red"])

# 3. "The orange book is the second from the right" → position 6
problem.addConstraint(lambda orange: orange == 6, ["orange"])

# 4. "The gray book is the fourth from the left" → position 4
problem.addConstraint(lambda gray: gray == 4, ["gray"])

# 5. "The black book is the rightmost" → position 7
problem.addConstraint(lambda black: black == 7, ["black"])

# 6. "The gray book is to the right of the red book" → red < gray
problem.addConstraint(lambda red, gray: red < gray, ["red", "gray"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to book names for the question about second-from-left (position 2)
choices = {
    'A': "orange",
    'B': "red",
    'C': "brown",
    'D': "blue",
    'E': "black",
    'F': "gray",
    'G': "white"
}

# Find which book is at position 2 and print the corresponding choice letter
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 2:
            print(letter)