from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (the seven books) and domain (positions 1 to 7)
books = ["purple", "brown", "red", "blue", "gray", "black", "green"]
positions = range(1, 8)
problem.addVariables(books, positions)

# Add constraints based on the problem description
# 1. All books must be in different positions
problem.addConstraint(AllDifferentConstraint())

# 2. "The brown book is to the left of the green book."
problem.addConstraint(lambda brown, green: brown < green, ("brown", "green"))

# 3. "The gray book is the second from the left."
problem.addConstraint(lambda gray: gray == 2, ("gray",))

# 4. "The black book is to the left of the gray book."
problem.addConstraint(lambda black, gray: black < gray, ("black", "gray"))

# 5. "The blue book is to the left of the red book."
problem.addConstraint(lambda blue, red: blue < red, ("blue", "red"))

# 6. "The blue book is the second from the right."
problem.addConstraint(lambda blue: blue == 6, ("blue",))

# 7. "The green book is to the left of the purple book."
problem.addConstraint(lambda green, purple: green < purple, ("green", "purple"))

# Get the solution(s)
solutions = problem.getSolutions()

# Map choice letters to book names
choices = {
    'A': 'purple',
    'B': 'brown',
    'C': 'red',
    'D': 'blue',
    'E': 'gray',
    'F': 'black',
    'G': 'green'
}

# Find which book is in position 3 (third from the left)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 3:
            print(letter)