from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=cheapest, 5=most expensive)
fruits = ["watermelons", "loquats", "pears", "plums", "apples"]
ranks = range(1, 6)
problem.addVariables(fruits, ranks)

# Add constraints based on the problem statements
# 1. All fruits have different price ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The pears are the second-cheapest" → pears == 2
problem.addConstraint(lambda pears: pears == 2, ["pears"])

# 3. "The loquats are more expensive than the pears" → loquats > pears
problem.addConstraint(lambda loquats, pears: loquats > pears, ["loquats", "pears"])

# 4. "The plums are the second-most expensive" → plums == 4
problem.addConstraint(lambda plums: plums == 4, ["plums"])

# 5. "The watermelons are the most expensive" → watermelons == 5
problem.addConstraint(lambda watermelons: watermelons == 5, ["watermelons"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to fruit names
choices = {
    "A": "watermelons",
    "B": "loquats",
    "C": "pears",
    "D": "plums",
    "E": "apples"
}

# Find the fruit with rank 1 (cheapest) and print corresponding choice letter
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 1:
            print(letter)