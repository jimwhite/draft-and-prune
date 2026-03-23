from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (the seven books) and domain (positions 1 to 7)
books = ["purple", "brown", "red", "blue", "gray", "black", "green"]
positions = range(1, 8)
problem.addVariables(books, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "The brown book is to the left of the green book."
problem.addConstraint(lambda brown, green: brown < green, ("brown", "green"))

# "The gray book is the second from the left."
problem.addConstraint(lambda gray: gray == 2, ("gray",))

# "The black book is to the left of the gray book."
problem.addConstraint(lambda black, gray: black < gray, ("black", "gray"))

# "The blue book is to the left of the red book."
problem.addConstraint(lambda blue, red: blue < red, ("blue", "red"))

# "The blue book is the second from the right." (position 6 in a 7-position shelf)
problem.addConstraint(lambda blue: blue == 6, ("blue",))

# "The green book is to the left of the purple book."
problem.addConstraint(lambda green, purple: green < purple, ("green", "purple"))

# Solve the problem
solutions = problem.getSolutions()

# Determine third from the right (position 5 in a 7-position shelf)
third_from_right = 5

# Map choice letters to book names
choices = {
    "A": "purple",
    "B": "brown",
    "C": "red",
    "D": "blue",
    "E": "gray",
    "F": "black",
    "G": "green"
}

# Find which book is at position 5 and print the corresponding choice letter
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == third_from_right:
            print(letter)