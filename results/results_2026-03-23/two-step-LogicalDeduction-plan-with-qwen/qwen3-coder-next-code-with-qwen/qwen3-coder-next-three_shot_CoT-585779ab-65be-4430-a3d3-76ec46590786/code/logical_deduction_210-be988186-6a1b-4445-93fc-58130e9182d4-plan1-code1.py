from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (books) and domain (positions 1 to 7)
books = ["black", "yellow", "white", "gray", "purple", "orange", "green"]
positions = range(1, 8)
problem.addVariables(books, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# 1. "The green book is to the left of the gray book" → green < gray
problem.addConstraint(lambda green, gray: green < gray, ["green", "gray"])

# 2. "The gray book is the third from the right" → gray position = 5 (positions: 1,2,3,4,5,6,7)
problem.addConstraint(lambda gray: gray == 5, ["gray"])

# 3. "The white book is the rightmost" → white position = 7
problem.addConstraint(lambda white: white == 7, ["white"])

# 4. "The orange book is the second from the left" → orange position = 2
problem.addConstraint(lambda orange: orange == 2, ["orange"])

# 5. "The black book is to the right of the yellow book" → black > yellow
problem.addConstraint(lambda yellow, black: black > yellow, ["yellow", "black"])

# 6. "The black book is the third from the left" → black position = 3
problem.addConstraint(lambda black: black == 3, ["black"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to book names
choices = {
    'A': 'black',
    'B': 'yellow',
    'C': 'white',
    'D': 'gray',
    'E': 'purple',
    'F': 'orange',
    'G': 'green'
}

# Find which book is at position 7 (rightmost)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 7:
            print(letter)