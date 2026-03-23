from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
books = ["white", "orange", "yellow", "blue", "red"]
positions = range(1, 6)
problem.addVariables(books, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The yellow book is to the left of the white book"
problem.addConstraint(lambda yellow, white: yellow < white, ("yellow", "white"))

# "The red book is to the right of the blue book"
problem.addConstraint(lambda blue, red: blue < red, ("blue", "red"))

# "The yellow book is to the right of the orange book"
problem.addConstraint(lambda orange, yellow: orange < yellow, ("orange", "yellow"))

# "The blue book is to the right of the white book"
problem.addConstraint(lambda white, blue: white < blue, ("white", "blue"))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to book names
choices = {
    "A": "white",
    "B": "orange",
    "C": "yellow",
    "D": "blue",
    "E": "red"
}

# Find which book is in position 4 (second from the right)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 4:
            print(letter)