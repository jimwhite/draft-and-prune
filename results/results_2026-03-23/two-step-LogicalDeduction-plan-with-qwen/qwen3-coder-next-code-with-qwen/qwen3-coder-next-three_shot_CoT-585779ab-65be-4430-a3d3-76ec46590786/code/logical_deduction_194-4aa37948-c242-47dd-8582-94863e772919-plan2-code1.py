from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (the seven books) and domain (positions 1 to 7)
books = ["black", "orange", "yellow", "white", "blue", "red", "green"]
positions = range(1, 8)
problem.addVariables(books, positions)

# Add constraints
# All books must be in different positions
problem.addConstraint(AllDifferentConstraint())

# "The red book is to the right of the yellow book"
problem.addConstraint(lambda r, y: r > y, ("red", "yellow"))

# "The white book is the second from the right"
problem.addConstraint(lambda w: w == 6, ("white",))

# "The red book is to the left of the green book"
problem.addConstraint(lambda r, g: r < g, ("red", "green"))

# "The blue book is to the right of the black book"
problem.addConstraint(lambda b, k: b > k, ("blue", "black"))

# "The black book is the third from the right"
problem.addConstraint(lambda k: k == 5, ("black",))

# "The orange book is the leftmost"
problem.addConstraint(lambda o: o == 1, ("orange",))

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

# Find which book is at position 3 (third from the left)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 3:
            print(letter)