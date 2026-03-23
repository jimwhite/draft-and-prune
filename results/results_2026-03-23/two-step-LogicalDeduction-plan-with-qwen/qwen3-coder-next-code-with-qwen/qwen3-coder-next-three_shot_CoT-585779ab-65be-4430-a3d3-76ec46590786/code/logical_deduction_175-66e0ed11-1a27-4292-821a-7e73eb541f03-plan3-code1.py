from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (books) and domain (positions 1 to 7)
books = ["red", "purple", "green", "white", "orange", "blue", "gray"]
positions = range(1, 8)
problem.addVariables(books, positions)

# Add AllDifferent constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# "The green book is to the left of the white book"
problem.addConstraint(lambda green, white: green < white, ("green", "white"))

# "The red book is to the left of the purple book"
problem.addConstraint(lambda red, purple: red < purple, ("red", "purple"))

# "The red book is to the right of the orange book"
problem.addConstraint(lambda orange, red: orange < red, ("orange", "red"))

# "The gray book is the second from the left"
problem.addConstraint(lambda gray: gray == 2, ("gray",))

# "The purple book is to the left of the green book"
problem.addConstraint(lambda purple, green: purple < green, ("purple", "green"))

# "The blue book is the fourth from the left"
problem.addConstraint(lambda blue: blue == 4, ("blue",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to book names
choices = {
    "A": "red",
    "B": "purple",
    "C": "green",
    "D": "white",
    "E": "orange",
    "F": "blue",
    "G": "gray"
}

# Find which book is in position 6 (second from the right)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 6:
            print(letter)