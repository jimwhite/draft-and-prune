from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (the seven books) and domain (positions 1 to 7)
books = ["orange", "red", "green", "white", "purple", "brown", "yellow"]
positions = range(1, 8)
problem.addVariables(books, positions)

# Add AllDifferent constraint to ensure each book is in a unique position
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "The green book is to the left of the purple book" → green < purple
problem.addConstraint(lambda green, purple: green < purple, ("green", "purple"))

# "The white book is to the right of the orange book" → white > orange
problem.addConstraint(lambda orange, white: orange < white, ("orange", "white"))

# "The green book is to the right of the brown book" → green > brown
problem.addConstraint(lambda brown, green: brown < green, ("brown", "green"))

# "The yellow book is to the right of the white book" → yellow > white
problem.addConstraint(lambda white, yellow: white < yellow, ("white", "yellow"))

# "The red book is to the right of the yellow book" → red > yellow
problem.addConstraint(lambda yellow, red: yellow < red, ("yellow", "red"))

# "The brown book is to the right of the red book" → brown > red
problem.addConstraint(lambda red, brown: red < brown, ("red", "brown"))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to book names for position 2 (second from left)
choices = {
    "A": "orange",
    "B": "red",
    "C": "green",
    "D": "white",
    "E": "purple",
    "F": "brown",
    "G": "yellow"
}

# Find which book is at position 2 and print the corresponding letter
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 2:
            print(letter)