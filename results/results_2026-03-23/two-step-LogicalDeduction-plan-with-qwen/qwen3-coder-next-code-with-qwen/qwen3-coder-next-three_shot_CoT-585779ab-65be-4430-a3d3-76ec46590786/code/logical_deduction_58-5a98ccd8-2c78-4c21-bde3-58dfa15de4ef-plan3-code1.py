from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (books) and domain (positions 1 to 5)
books = ["brown", "orange", "red", "purple", "black"]
positions = range(1, 6)
problem.addVariables(books, positions)

# Add constraints based on the statements
# All books must be in different positions
problem.addConstraint(AllDifferentConstraint())

# The purple book is to the left of the black book
problem.addConstraint(lambda purple, black: purple < black, ("purple", "black"))

# The red book is to the right of the brown book
problem.addConstraint(lambda brown, red: brown < red, ("brown", "red"))

# The orange book is the second from the left
problem.addConstraint(lambda orange: orange == 2, ("orange",))

# The black book is the third from the left
problem.addConstraint(lambda black: black == 3, ("black",))

# Solve the problem
solutions = problem.getSolutions()

# The question asks which book is the second from the left (position 2)
# According to the statement, orange == 2, so choice B should be correct
choices = {
    "A": "brown",
    "B": "orange",
    "C": "red",
    "D": "purple",
    "E": "black"
}

# Find which book is at position 2 and print the corresponding letter
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 2:
            print(letter)