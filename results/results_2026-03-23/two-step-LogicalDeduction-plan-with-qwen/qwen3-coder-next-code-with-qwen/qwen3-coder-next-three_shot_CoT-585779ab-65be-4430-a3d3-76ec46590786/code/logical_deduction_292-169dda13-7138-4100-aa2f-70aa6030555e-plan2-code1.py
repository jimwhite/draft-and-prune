from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
fruits = ["apples", "pears", "loquats"]
ranks = range(1, 4)  # 1=least expensive, 3=most expensive
problem.addVariables(fruits, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The pears are more expensive than the loquats" -> loquats < pears
problem.addConstraint(lambda loquats, pears: loquats < pears, ("loquats", "pears"))

# "The pears are less expensive than the apples" -> pears < apples
problem.addConstraint(lambda pears, apples: pears < apples, ("pears", "apples"))

# Solve the problem
solutions = problem.getSolutions()

# Map choices to fruit names
choices = {
    "A": "apples",
    "B": "pears",
    "C": "loquats"
}

# Find the most expensive fruit (rank 3) and print corresponding choice letter
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 3:
            print(letter)