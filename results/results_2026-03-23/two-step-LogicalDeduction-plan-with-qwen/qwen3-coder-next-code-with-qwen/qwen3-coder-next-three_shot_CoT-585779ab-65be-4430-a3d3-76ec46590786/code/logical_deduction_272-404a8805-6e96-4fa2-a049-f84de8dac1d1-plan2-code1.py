from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
fruits = ["apples", "peaches", "loquats"]
prices = [1, 2, 3]  # 1=least expensive, 2=second-most expensive, 3=most expensive
problem.addVariables(fruits, prices)

# Add constraints based on the statements
# All fruits have distinct prices
problem.addConstraint(AllDifferentConstraint())

# The loquats are less expensive than the apples: loquats < apples
problem.addConstraint(lambda loquats, apples: loquats < apples, ("loquats", "apples"))

# The peaches are more expensive than the apples: apples < peaches
problem.addConstraint(lambda apples, peaches: apples < peaches, ("apples", "peaches"))

# Solve the problem
solutions = problem.getSolutions()

# Map choices to fruits
choices = {
    "A": "apples",
    "B": "peaches",
    "C": "loquats"
}

# Find the fruit with rank 2 (second-most expensive)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 2:
            print(letter)