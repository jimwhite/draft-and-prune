from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (the seven books) and domain (positions 1 to 7)
books = ["black", "yellow", "white", "gray", "purple", "orange", "green"]
positions = range(1, 8)
problem.addVariables(books, positions)

# Add constraints based on the problem description
# 1. All books must be in different positions
problem.addConstraint(AllDifferentConstraint())

# 2. "The green book is to the left of the gray book."
problem.addConstraint(lambda green, gray: green < gray, ("green", "gray"))

# 3. "The gray book is the third from the right."
# In a set of 7, third from right = position 5 (since 7-2=5)
problem.addConstraint(lambda gray: gray == 5, ("gray",))

# 4. "The white book is the rightmost."
problem.addConstraint(lambda white: white == 7, ("white",))

# 5. "The orange book is the second from the left."
problem.addConstraint(lambda orange: orange == 2, ("orange",))

# 6. "The black book is to the right of the yellow book."
problem.addConstraint(lambda black, yellow: black > yellow, ("black", "yellow"))

# 7. "The black book is the third from the left."
problem.addConstraint(lambda black: black == 3, ("black",))

# Find all solutions and get the unique one
solutions = problem.getSolutions()
solution = solutions[0]

# Map choice letters to book names
choices = {
    'A': 'black',
    'B': 'yellow',
    'C': 'white',
    'D': 'gray',
    'E': 'purple',
    'F': 'orange',
    'G': 'green'
}

# Find which book is in position 4 (fourth from left)
for letter, book_name in choices.items():
    if solution[book_name] == 4:
        print(letter)