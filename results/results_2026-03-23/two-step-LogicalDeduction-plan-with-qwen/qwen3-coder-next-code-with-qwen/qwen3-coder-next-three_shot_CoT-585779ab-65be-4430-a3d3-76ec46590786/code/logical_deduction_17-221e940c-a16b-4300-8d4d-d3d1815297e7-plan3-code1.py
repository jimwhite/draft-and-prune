from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=cheapest, 5=most expensive)
fruits = ["watermelons", "apples", "mangoes", "pears", "cantaloupes"]
ranks = range(1, 6)
problem.addVariables(fruits, ranks)

# Add constraints based on the problem description
# 1. All fruits have different price ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The watermelons are more expensive than the cantaloupes"
problem.addConstraint(lambda watermelons, cantaloupes: watermelons > cantaloupes, ("watermelons", "cantaloupes"))

# 3. "The mangoes are less expensive than the pears"
problem.addConstraint(lambda mangoes, pears: mangoes < pears, ("mangoes", "pears"))

# 4. "The apples are the second-cheapest"
problem.addConstraint(lambda apples: apples == 2, ("apples",))

# 5. "The watermelons are less expensive than the mangoes"
problem.addConstraint(lambda watermelons, mangoes: watermelons < mangoes, ("watermelons", "mangoes"))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to fruit names
choices = {
    "A": "watermelons",
    "B": "apples",
    "C": "mangoes",
    "D": "pears",
    "E": "cantaloupes"
}

# Find which fruit has rank 1 (cheapest) and print the corresponding choice letter
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 1:
            print(letter)