from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=cheapest, 5=most expensive)
fruits = ["apples", "mangoes", "oranges", "plums", "pears"]
ranks = range(1, 6)
problem.addVariables(fruits, ranks)

# Add constraints based on the statements
# All fruits have different price ranks
problem.addConstraint(AllDifferentConstraint())

# "The oranges are more expensive than the mangoes" → oranges > mangoes
problem.addConstraint(lambda mangoes, oranges: mangoes < oranges, ["mangoes", "oranges"])

# "The plums are the cheapest" → plums == 1
problem.addConstraint(lambda plums: plums == 1, ["plums"])

# "The apples are less expensive than the mangoes" → apples < mangoes
problem.addConstraint(lambda apples, mangoes: apples < mangoes, ["apples", "mangoes"])

# "The pears are more expensive than the oranges" → pears > oranges
problem.addConstraint(lambda oranges, pears: oranges < pears, ["oranges", "pears"])

# Solve the puzzle
solutions = problem.getSolutions()

# Map choice letters to fruit names
choices = {
    "A": "apples",
    "B": "mangoes",
    "C": "oranges",
    "D": "plums",
    "E": "pears"
}

# Find which fruit is the cheapest (rank 1) and print corresponding choice letter
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 1:
            print(letter)