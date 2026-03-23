from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (books) and domain (positions 1 to 7)
books = ["black", "orange", "yellow", "white", "blue", "red", "green"]
positions = range(1, 8)
problem.addVariables(books, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "The orange book is the leftmost" → position 1
problem.addConstraint(lambda orange: orange == 1, ["orange"])

# "The black book is the third from the right" → position 5 (since 7-2=5)
problem.addConstraint(lambda black: black == 5, ["black"])

# "The white book is the second from the right" → position 6
problem.addConstraint(lambda white: white == 6, ["white"])

# "The red book is to the right of the yellow book" → yellow < red
problem.addConstraint(lambda yellow, red: yellow < red, ["yellow", "red"])

# "The red book is to the left of the green book" → red < green
problem.addConstraint(lambda red, green: red < green, ["red", "green"])

# "The blue book is to the right of the black book" → black < blue
problem.addConstraint(lambda black, blue: black < blue, ["black", "blue"])

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

# Find which book is in position 3 (third from the left)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 3:
            print(letter)