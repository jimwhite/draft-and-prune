from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=cheapest, 3=most expensive)
fruits = ["apples", "peaches", "loquats"]
ranks = range(1, 4)
problem.addVariables(fruits, ranks)

# Add constraints based on the problem description
# 1. All fruits must have different price ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The loquats are less expensive than the apples" → loquats < apples
problem.addConstraint(lambda loquats, apples: loquats < apples, ("loquats", "apples"))

# 3. "The peaches are more expensive than the apples" → apples < peaches
problem.addConstraint(lambda apples, peaches: apples < peaches, ("apples", "peaches"))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to fruit names
choices = {
    "A": "apples",
    "B": "peaches",
    "C": "loquats"
}

# Find which fruit has rank 2 (second-most expensive)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 2:
            print(letter)