from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (price ranks 1=cheapest to 7=most expensive)
fruits = ["apples", "pears", "mangoes", "oranges", "watermelons", "peaches", "cantaloupes"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# Pears are more expensive than oranges: pears > oranges
problem.addConstraint(lambda pears, oranges: pears > oranges, ("pears", "oranges"))

# Oranges are more expensive than cantaloupes: oranges > cantaloupes
problem.addConstraint(lambda oranges, cantaloupes: oranges > cantaloupes, ("oranges", "cantaloupes"))

# Peaches are less expensive than cantaloupes: peaches < cantaloupes
problem.addConstraint(lambda peaches, cantaloupes: peaches < cantaloupes, ("peaches", "cantaloupes"))

# Apples are the third-cheapest: apples == 3
problem.addConstraint(lambda apples: apples == 3, ("apples",))

# Watermelons are the second-most expensive: watermelons == 6
problem.addConstraint(lambda watermelons: watermelons == 6, ("watermelons",))

# Mangoes are the fourth-most expensive: mangoes == 4
problem.addConstraint(lambda mangoes: mangoes == 4, ("mangoes",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to fruit names
choices = {
    "A": "apples",
    "B": "pears",
    "C": "mangoes",
    "D": "oranges",
    "E": "watermelons",
    "F": "peaches",
    "G": "cantaloupes"
}

# Find which fruit is the second-cheapest (rank 2)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 2:
            print(letter)