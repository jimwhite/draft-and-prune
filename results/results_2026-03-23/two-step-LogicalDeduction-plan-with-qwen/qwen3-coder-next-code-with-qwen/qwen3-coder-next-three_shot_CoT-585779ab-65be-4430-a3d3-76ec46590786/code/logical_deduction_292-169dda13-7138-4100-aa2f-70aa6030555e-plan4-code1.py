from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=least expensive, 3=most expensive)
fruits = ["apples", "pears", "loquats"]
ranks = [1, 2, 3]
problem.addVariables(fruits, ranks)

# Add constraints based on the problem description
# 1. All fruits must have different price ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The pears are more expensive than the loquats" → pears > loquats
problem.addConstraint(lambda pears, loquats: pears > loquats, ["pears", "loquats"])

# 3. "The pears are less expensive than the apples" → pears < apples
problem.addConstraint(lambda pears, apples: pears < apples, ["pears", "apples"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to fruits
choices = {
    "A": "apples",
    "B": "pears",
    "C": "loquats"
}

# Find which fruit has the highest price rank (3) and print corresponding choice letter
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 3:
            print(letter)