from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (books) and domain (positions 1 to 7)
books = ["orange", "red", "brown", "blue", "black", "gray", "white"]
positions = range(1, 8)
problem.addVariables(books, positions)

# Add AllDifferentConstraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# "The white book is the leftmost" → white == 1
problem.addConstraint(lambda white: white == 1, ["white"])

# "The red book is to the right of the blue book" → blue < red
problem.addConstraint(lambda blue, red: blue < red, ["blue", "red"])

# "The orange book is the second from the right" → orange == 6
problem.addConstraint(lambda orange: orange == 6, ["orange"])

# "The gray book is the fourth from the left" → gray == 4
problem.addConstraint(lambda gray: gray == 4, ["gray"])

# "The black book is the rightmost" → black == 7
problem.addConstraint(lambda black: black == 7, ["black"])

# "The gray book is to the right of the red book" → red < gray
problem.addConstraint(lambda red, gray: red < gray, ["red", "gray"])

# Solve the problem
solutions = problem.getSolutions()

# Get the first (and only) solution
solution = solutions[0]

# Map choice letters to book names
choices = {
    'A': "orange",
    'B': "red",
    'C': "brown",
    'D': "blue",
    'E': "black",
    'F': "gray",
    'G': "white"
}

# Find which book is at position 4 (fourth from the left)
for letter, book_name in choices.items():
    if solution[book_name] == 4:
        print(letter)