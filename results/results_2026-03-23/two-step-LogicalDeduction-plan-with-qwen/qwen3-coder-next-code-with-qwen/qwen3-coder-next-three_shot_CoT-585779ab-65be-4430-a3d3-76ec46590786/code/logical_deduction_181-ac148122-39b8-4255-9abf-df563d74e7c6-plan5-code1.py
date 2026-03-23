from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define the seven books as variables
books = ["orange", "red", "brown", "blue", "black", "gray", "white"]

# Define the domain: positions 1 to 7 (1 = leftmost, 7 = rightmost)
positions = range(1, 8)
problem.addVariables(books, positions)

# Add constraints based on the problem description
# 1. All books must be in different positions
problem.addConstraint(AllDifferentConstraint())

# 2. "The white book is the leftmost" → white == 1
problem.addConstraint(lambda white: white == 1, ["white"])

# 3. "The red book is to the right of the blue book" → blue < red
problem.addConstraint(lambda blue, red: blue < red, ["blue", "red"])

# 4. "The orange book is the second from the right" → orange == 6
problem.addConstraint(lambda orange: orange == 6, ["orange"])

# 5. "The gray book is the fourth from the left" → gray == 4
problem.addConstraint(lambda gray: gray == 4, ["gray"])

# 6. "The black book is the rightmost" → black == 7
problem.addConstraint(lambda black: black == 7, ["black"])

# 7. "The gray book is to the right of the red book" → red < gray
problem.addConstraint(lambda red, gray: red < gray, ["red", "gray"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to book names for the second-from-left position (position 2)
choices = {
    "A": "orange",
    "B": "red",
    "C": "brown",
    "D": "blue",
    "E": "black",
    "F": "gray",
    "G": "white"
}

# Find which book is at position 2 and print the corresponding choice letter
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 2:
            print(letter)