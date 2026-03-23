from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (the seven books) and domain (positions 1 to 7)
books = ["red", "purple", "green", "white", "orange", "blue", "gray"]
positions = range(1, 8)
problem.addVariables(books, positions)

# Add constraints based on the problem description
# 1. All books must be in different positions
problem.addConstraint(AllDifferentConstraint())

# 2. "The green book is to the left of the white book."
problem.addConstraint(lambda green, white: green < white, ("green", "white"))

# 3. "The red book is to the left of the purple book."
problem.addConstraint(lambda red, purple: red < purple, ("red", "purple"))

# 4. "The red book is to the right of the orange book."
problem.addConstraint(lambda orange, red: orange < red, ("orange", "red"))

# 5. "The gray book is the second from the left."
problem.addConstraint(lambda gray: gray == 2, ("gray",))

# 6. "The purple book is to the left of the green book."
problem.addConstraint(lambda purple, green: purple < green, ("purple", "green"))

# 7. "The blue book is the fourth from the left."
problem.addConstraint(lambda blue: blue == 4, ("blue",))

# Get all solutions and extract the first (and only) solution
solutions = problem.getSolutions()
solution = solutions[0]

# Map choice letters to book names
choices = {
    'A': 'red',
    'B': 'purple',
    'C': 'green',
    'D': 'white',
    'E': 'orange',
    'F': 'blue',
    'G': 'gray'
}

# Find which book is at position 7 (rightmost)
for letter, book_name in choices.items():
    if solution[book_name] == 7:
        print(letter)