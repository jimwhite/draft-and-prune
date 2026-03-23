from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
fruits = ["apples", "peaches", "loquats"]
ranks = range(1, 4)  # 1=least expensive, 2=second-most expensive, 3=most expensive
problem.addVariables(fruits, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The loquats are less expensive than the apples" -> loquats rank < apples rank
problem.addConstraint(lambda loquats, apples: loquats < apples, ("loquats", "apples"))

# "The peaches are more expensive than the apples" -> apples rank < peaches rank
problem.addConstraint(lambda apples, peaches: apples < peaches, ("apples", "peaches"))

# Solve for the unique ordering
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