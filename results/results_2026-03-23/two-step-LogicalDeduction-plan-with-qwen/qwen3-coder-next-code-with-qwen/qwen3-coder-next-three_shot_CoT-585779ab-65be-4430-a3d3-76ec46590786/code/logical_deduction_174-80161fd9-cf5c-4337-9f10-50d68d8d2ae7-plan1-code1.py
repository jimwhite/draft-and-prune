from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables (the seven fruits) and domain (price positions 1 to 7)
fruits = ["loquats", "cantaloupes", "watermelons", "apples", "oranges", "pears", "mangoes"]
positions = range(1, 8)
problem.addVariables(fruits, positions)

# Add constraints based on the problem description
# 1. All fruits have different price positions
problem.addConstraint(AllDifferentConstraint())

# 2. "The oranges are the second-cheapest" → position 2
problem.addConstraint(lambda oranges: oranges == 2, ["oranges"])

# 3. "The apples are less expensive than the pears" → apples < pears
problem.addConstraint(lambda apples, pears: apples < pears, ["apples", "pears"])

# 4. "The mangoes are more expensive than the cantaloupes" → cantaloupes < mangoes
problem.addConstraint(lambda cantaloupes, mangoes: cantaloupes < mangoes, ["cantaloupes", "mangoes"])

# 5. "The mangoes are the third-cheapest" → position 3
problem.addConstraint(lambda mangoes: mangoes == 3, ["mangoes"])

# 6. "The watermelons are the second-most expensive" → position 6
problem.addConstraint(lambda watermelons: watermelons == 6, ["watermelons"])

# 7. "The loquats are the third-most expensive" → position 5
problem.addConstraint(lambda loquats: loquats == 5, ["loquats"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to fruit names
choices = {
    "A": "loquats",
    "B": "cantaloupes",
    "C": "watermelons",
    "D": "apples",
    "E": "oranges",
    "F": "pears",
    "G": "mangoes"
}

# Find which fruit is at position 5 (third-most expensive)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 5:
            print(letter)