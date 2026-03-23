from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables and domain
fruits = ["apples", "pears", "loquats"]
ranks = range(1, 4)  # 1=cheapest, 3=most expensive
problem.addVariables(fruits, ranks)

# Add constraints based on the problem description
# 1. All fruits must have different price ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The pears are more expensive than the loquats" → pears > loquats
problem.addConstraint(lambda loquats, pears: loquats < pears, ("loquats", "pears"))

# 3. "The pears are less expensive than the apples" → pears < apples
problem.addConstraint(lambda pears, apples: pears < apples, ("pears", "apples"))

# Solve for the ordering
solutions = problem.getSolutions()

# Map choices to fruits
choices = {
    "A": "apples",
    "B": "pears",
    "C": "loquats"
}

# Find which fruit is most expensive (rank 3)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 3:
            print(letter)