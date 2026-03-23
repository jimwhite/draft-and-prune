from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (books) and domain (positions 1 to 7)
books = ["black", "orange", "yellow", "white", "blue", "red", "green"]
positions = range(1, 8)
problem.addVariables(books, positions)

# Add all different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem description:
# 1. "The red book is to the right of the yellow book" → red > yellow
problem.addConstraint(lambda yellow, red: yellow < red, ("yellow", "red"))

# 2. "The white book is the second from the right" → white == 6
problem.addConstraint(lambda white: white == 6, ("white",))

# 3. "The red book is to the left of the green book" → red < green
problem.addConstraint(lambda red, green: red < green, ("red", "green"))

# 4. "The blue book is to the right of the black book" → blue > black
problem.addConstraint(lambda black, blue: black < blue, ("black", "blue"))

# 5. "The black book is the third from the right" → black == 5
problem.addConstraint(lambda black: black == 5, ("black",))

# 6. "The orange book is the leftmost" → orange == 1
problem.addConstraint(lambda orange: orange == 1, ("orange",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to book names
choices = {
    "A": "black",
    "B": "orange",
    "C": "yellow",
    "D": "white",
    "E": "blue",
    "F": "red",
    "G": "green"
}

# Find which book is at position 7 (rightmost)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 7:
            print(letter)