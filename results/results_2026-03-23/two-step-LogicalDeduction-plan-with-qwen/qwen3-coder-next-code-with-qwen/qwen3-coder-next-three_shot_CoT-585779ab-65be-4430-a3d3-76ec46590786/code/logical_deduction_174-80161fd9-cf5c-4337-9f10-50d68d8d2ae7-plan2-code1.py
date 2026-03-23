from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define the seven fruits as variables
fruits = ["loquats", "cantaloupes", "watermelons", "apples", "oranges", "pears", "mangoes"]

# Define the domain: integers 1 to 7, where 1 = cheapest and 7 = most expensive
prices = range(1, 8)
problem.addVariables(fruits, prices)

# Add constraints based on the problem description
# 1. All fruits have different price ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The oranges are the second-cheapest"
problem.addConstraint(lambda oranges: oranges == 2, ["oranges"])

# 3. "The apples are less expensive than the pears"
problem.addConstraint(lambda apples, pears: apples < pears, ["apples", "pears"])

# 4. "The mangoes are more expensive than the cantaloupes"
problem.addConstraint(lambda cantaloupes, mangoes: cantaloupes < mangoes, ["cantaloupes", "mangoes"])

# 5. "The mangoes are the third-cheapest"
problem.addConstraint(lambda mangoes: mangoes == 3, ["mangoes"])

# 6. "The watermelons are the second-most expensive"
problem.addConstraint(lambda watermelons: watermelons == 6, ["watermelons"])

# 7. "The loquats are the third-most expensive"
problem.addConstraint(lambda loquats: loquats == 5, ["loquats"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to fruit names
choices = {
    "A": "loquats",
    "B": "cantaloupes",
    "C": "watermelons",
    "D": "apples",
    "E": "oranges",
    "F": "pears",
    "G": "mangoes"
}

# Find which fruit is third-most expensive (rank = 5)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 5:
            print(letter)