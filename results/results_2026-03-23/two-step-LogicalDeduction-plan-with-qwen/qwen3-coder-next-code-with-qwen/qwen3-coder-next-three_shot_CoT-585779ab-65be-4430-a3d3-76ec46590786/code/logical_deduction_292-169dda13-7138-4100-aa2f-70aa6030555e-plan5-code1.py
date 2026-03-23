from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
fruits = ["apples", "pears", "loquats"]
ranks = range(1, 4)  # 1=cheapest, 2=middle, 3=most expensive
problem.addVariables(fruits, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# Pears are more expensive than loquats: pears > loquats
problem.addConstraint(lambda pears, loquats: pears > loquats, ("pears", "loquats"))

# Pears are less expensive than apples: pears < apples
problem.addConstraint(lambda pears, apples: pears < apples, ("pears", "apples"))

# Solve the problem
solutions = problem.getSolutions()

# Map choices to fruits
choices = {
    "A": "apples",
    "B": "pears",
    "C": "loquats"
}

# Find the fruit with rank 3 (most expensive)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 3:
            print(letter)