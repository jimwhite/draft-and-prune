from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=cheapest, 5=most expensive)
fruits = ["watermelons", "loquats", "pears", "plums", "apples"]
ranks = range(1, 6)
problem.addVariables(fruits, ranks)

# Add constraints based on the problem description
# 1. All fruits have different price ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The pears are the second-cheapest" → rank 2
problem.addConstraint(lambda pears: pears == 2, ["pears"])

# 3. "The loquats are more expensive than the pears" → loquats > pears
problem.addConstraint(lambda loquats, pears: loquats > pears, ["loquats", "pears"])

# 4. "The plums are the second-most expensive" → rank 4
problem.addConstraint(lambda plums: plums == 4, ["plums"])

# 5. "The watermelons are the most expensive" → rank 5
problem.addConstraint(lambda watermelons: watermelons == 5, ["watermelons"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to fruit names for the cheapest position (rank 1)
choices = {
    "A": "watermelons",
    "B": "loquats",
    "C": "pears",
    "D": "plums",
    "E": "apples"
}

# Find which fruit has rank 1 (cheapest) and print the corresponding choice letter
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 1:
            print(letter)