from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=cheapest, 7=most expensive)
fruits = ["loquats", "cantaloupes", "watermelons", "apples", "oranges", "pears", "mangoes"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add AllDifferent constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem statements:
# 1. The oranges are the second-cheapest (rank 2)
problem.addConstraint(lambda oranges: oranges == 2, ["oranges"])

# 2. The apples are less expensive than the pears (apples rank < pears rank)
problem.addConstraint(lambda apples, pears: apples < pears, ["apples", "pears"])

# 3. The mangoes are more expensive than the cantaloupes (mangoes rank > cantaloupes rank)
problem.addConstraint(lambda cantaloupes, mangoes: cantaloupes < mangoes, ["cantaloupes", "mangoes"])

# 4. The mangoes are the third-cheapest (rank 3)
problem.addConstraint(lambda mangoes: mangoes == 3, ["mangoes"])

# 5. The watermelons are the second-most expensive (rank 6)
problem.addConstraint(lambda watermelons: watermelons == 6, ["watermelons"])

# 6. The loquats are the third-most expensive (rank 5)
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

# Find which fruit has rank 5 (third-most expensive)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 5:
            print(letter)