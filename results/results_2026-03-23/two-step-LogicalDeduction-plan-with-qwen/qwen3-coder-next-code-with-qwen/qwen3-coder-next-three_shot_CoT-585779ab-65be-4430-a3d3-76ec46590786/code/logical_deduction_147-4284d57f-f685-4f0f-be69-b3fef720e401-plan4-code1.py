from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (books) and domain (positions 1 to 7, where 1=leftmost, 7=rightmost)
books = ["brown", "yellow", "black", "white", "green", "orange", "purple"]
positions = range(1, 8)
problem.addVariables(books, positions)

# Add AllDifferentConstraint to ensure each book is in a unique position
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem statements:
# "The purple book is the rightmost" → position 7
problem.addConstraint(lambda purple: purple == 7, ["purple"])

# "The yellow book is the leftmost" → position 1
problem.addConstraint(lambda yellow: yellow == 1, ["yellow"])

# "The orange book is the second from the right" → position 6
problem.addConstraint(lambda orange: orange == 6, ["orange"])

# "The brown book is to the left of the green book" → brown < green
problem.addConstraint(lambda brown, green: brown < green, ["brown", "green"])

# "The brown book is to the right of the black book" → black < brown
problem.addConstraint(lambda black, brown: black < brown, ["black", "brown"])

# "The white book is the fourth from the left" → position 4
problem.addConstraint(lambda white: white == 4, ["white"])

# Solve the problem
solutions = problem.getSolutions()

# Map answer choices to book names
choices = {
    "A": "brown",
    "B": "yellow",
    "C": "black",
    "D": "white",
    "E": "green",
    "F": "orange",
    "G": "purple"
}

# Find which book is third from the right (position 5 in a 7-position sequence)
for solution in solutions:
    for letter, book_name in choices.items():
        if solution[book_name] == 5:
            print(letter)