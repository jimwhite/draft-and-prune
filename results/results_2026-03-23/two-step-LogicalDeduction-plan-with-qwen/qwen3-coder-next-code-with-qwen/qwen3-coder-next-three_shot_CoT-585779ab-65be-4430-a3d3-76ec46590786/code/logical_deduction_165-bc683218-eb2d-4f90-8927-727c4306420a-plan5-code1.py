from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (books) and domain (positions 1 to 7)
books = ["orange", "red", "brown", "blue", "black", "gray", "white"]
positions = range(1, 8)
problem.addVariables(books, positions)

# Add AllDifferent constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# 1. "The white book is the leftmost" → white == 1
problem.addConstraint(lambda w: w == 1, ["white"])

# 2. "The red book is to the right of the blue book" → blue < red
problem.addConstraint(lambda b, r: b < r, ["blue", "red"])

# 3. "The orange book is the second from the right" → orange == 6
problem.addConstraint(lambda o: o == 6, ["orange"])

# 4. "The gray book is the fourth from the left" → gray == 4
problem.addConstraint(lambda g: g == 4, ["gray"])

# 5. "The black book is the rightmost" → black == 7
problem.addConstraint(lambda bk: bk == 7, ["black"])

# 6. "The gray book is to the right of the red book" → red < gray
problem.addConstraint(lambda r, g: r < g, ["red", "gray"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to book names
choices = {
    'A': "orange",
    'B': "red",
    'C': "brown",
    'D': "blue",
    'E': "black",
    'F': "gray",
    'G': "white"
}

# Find which book is at position 4 (fourth from the left)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 4:
            print(letter)