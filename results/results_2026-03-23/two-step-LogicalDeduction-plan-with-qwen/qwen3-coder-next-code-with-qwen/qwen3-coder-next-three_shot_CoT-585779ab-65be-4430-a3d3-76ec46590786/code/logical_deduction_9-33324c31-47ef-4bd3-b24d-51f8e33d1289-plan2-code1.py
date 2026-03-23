from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (books) and domain (positions 1 to 5, where 1=leftmost, 5=rightmost)
books = ["brown", "orange", "red", "purple", "black"]
positions = range(1, 6)
problem.addVariables(books, positions)

# Add constraints based on the problem description
# 1. All books must be in different positions
problem.addConstraint(AllDifferentConstraint())

# 2. The purple book is to the left of the black book
problem.addConstraint(lambda purple, black: purple < black, ("purple", "black"))

# 3. The red book is to the right of the brown book
problem.addConstraint(lambda brown, red: brown < red, ("brown", "red"))

# 4. The orange book is the second from the left (position 2)
problem.addConstraint(lambda orange: orange == 2, ("orange",))

# 5. The black book is the third from the left (position 3)
problem.addConstraint(lambda black: black == 3, ("black",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to book names for the question about second from right (position 4)
choices = {
    "A": "brown",
    "B": "orange",
    "C": "red",
    "D": "purple",
    "E": "black"
}

# Find which book is at position 4 (second from right) and print the corresponding letter
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 4:
            print(letter)