from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (books) and domain (positions 1 to 5, where 1 is leftmost, 5 is rightmost)
books = ["white", "orange", "yellow", "blue", "red"]
positions = range(1, 6)
problem.addVariables(books, positions)

# Add constraint that all books must be in different positions
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem statements:
# 1. "The yellow book is to the left of the white book" → yellow < white
problem.addConstraint(lambda yellow, white: yellow < white, ["yellow", "white"])

# 2. "The red book is to the right of the blue book" → blue < red
problem.addConstraint(lambda blue, red: blue < red, ["blue", "red"])

# 3. "The yellow book is to the right of the orange book" → orange < yellow
problem.addConstraint(lambda orange, yellow: orange < yellow, ["orange", "yellow"])

# 4. "The blue book is to the right of the white book" → white < blue
problem.addConstraint(lambda white, blue: white < blue, ["white", "blue"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to book names for the question about second from right (position 4)
choices = {
    "A": "white",
    "B": "orange",
    "C": "yellow",
    "D": "blue",
    "E": "red"
}

# Find which book is at position 4 (second from right) and print the corresponding letter
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 4:
            print(letter)