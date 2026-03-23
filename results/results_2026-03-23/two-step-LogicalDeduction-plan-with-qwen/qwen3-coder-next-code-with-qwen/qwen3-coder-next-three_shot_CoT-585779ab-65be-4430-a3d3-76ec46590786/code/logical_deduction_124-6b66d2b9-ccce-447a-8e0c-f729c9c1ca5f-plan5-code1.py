from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (the seven books) and domain (positions 1 to 7)
books = ["black", "orange", "yellow", "white", "blue", "red", "green"]
positions = range(1, 8)
problem.addVariables(books, positions)

# Add constraints based on the problem description
# 1. All books must be in different positions
problem.addConstraint(AllDifferentConstraint())

# 2. "The red book is to the right of the yellow book" → yellow < red
problem.addConstraint(lambda yellow, red: yellow < red, ("yellow", "red"))

# 3. "The white book is the second from the right" → white == 6
problem.addConstraint(lambda white: white == 6, ("white",))

# 4. "The red book is to the left of the green book" → red < green
problem.addConstraint(lambda red, green: red < green, ("red", "green"))

# 5. "The blue book is to the right of the black book" → black < blue
problem.addConstraint(lambda black, blue: black < blue, ("black", "blue"))

# 6. "The black book is the third from the right" → black == 5
problem.addConstraint(lambda black: black == 5, ("black",))

# 7. "The orange book is the leftmost" → orange == 1
problem.addConstraint(lambda orange: orange == 1, ("orange",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to book names
choices = {
    'A': 'black',
    'B': 'orange',
    'C': 'yellow',
    'D': 'white',
    'E': 'blue',
    'F': 'red',
    'G': 'green'
}

# Find which book is at position 7 (rightmost) and print the corresponding choice letter
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 7:
            print(letter)