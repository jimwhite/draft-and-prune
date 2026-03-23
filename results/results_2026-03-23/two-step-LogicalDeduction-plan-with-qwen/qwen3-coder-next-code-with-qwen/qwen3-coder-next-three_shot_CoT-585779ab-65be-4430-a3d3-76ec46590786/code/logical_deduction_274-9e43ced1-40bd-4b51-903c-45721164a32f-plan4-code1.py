from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=cheapest, 3=most expensive)
fruits = ["peaches", "pears", "mangoes"]
ranks = range(1, 4)
problem.addVariables(fruits, ranks)

# Add constraints based on the problem description
# 1. All fruits must have different price ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The peaches are the cheapest."
problem.addConstraint(lambda peaches: peaches == 1, ["peaches"])

# 3. "The mangoes are less expensive than the pears."
problem.addConstraint(lambda mangoes, pears: mangoes < pears, ["mangoes", "pears"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to fruit names
choices = {
    "A": "peaches",
    "B": "pears",
    "C": "mangoes"
}

# Find which fruit has rank 1 (cheapest) and print the corresponding letter
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 1:
            print(letter)