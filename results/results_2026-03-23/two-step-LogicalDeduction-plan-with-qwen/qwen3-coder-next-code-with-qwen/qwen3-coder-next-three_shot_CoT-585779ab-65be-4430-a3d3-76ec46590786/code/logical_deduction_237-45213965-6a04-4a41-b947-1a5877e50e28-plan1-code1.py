from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (books) and domain (positions 1 to 7)
books = ["red", "white", "purple", "black", "gray", "orange", "blue"]
positions = range(1, 8)
problem.addVariables(books, positions)

# Add AllDifferent constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# "The red book is to the right of the white book" → red > white
problem.addConstraint(lambda red, white: red > white, ("red", "white"))

# "The gray book is to the left of the orange book" → gray < orange
problem.addConstraint(lambda gray, orange: gray < orange, ("gray", "orange"))

# "The gray book is to the right of the blue book" → gray > blue
problem.addConstraint(lambda gray, blue: gray > blue, ("gray", "blue"))

# "The red book is the second from the right" → red == 6
problem.addConstraint(lambda red: red == 6, ("red",))

# "The black book is the fourth from the left" → black == 4
problem.addConstraint(lambda black: black == 4, ("black",))

# "The orange book is to the left of the white book" → orange < white
problem.addConstraint(lambda orange, white: orange < white, ("orange", "white"))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to book names
choices = {
    'A': 'red',
    'B': 'white',
    'C': 'purple',
    'D': 'black',
    'E': 'gray',
    'F': 'orange',
    'G': 'blue'
}

# Find which book is at position 5 (third from the right in a 7-position shelf)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 5:
            print(letter)