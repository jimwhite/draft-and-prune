from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=cheapest, 5=most expensive)
fruits = ["watermelons", "apples", "kiwis", "cantaloupes", "mangoes"]
ranks = range(1, 6)
problem.addVariables(fruits, ranks)

# Add constraints based on the problem description
# 1. All fruits have different price ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The cantaloupes are the second-cheapest" → rank = 2
problem.addConstraint(lambda cantaloupes: cantaloupes == 2, ["cantaloupes"])

# 3. "The mangoes are more expensive than the watermelons" → watermelons < mangoes
problem.addConstraint(lambda watermelons, mangoes: watermelons < mangoes, ["watermelons", "mangoes"])

# 4. "The kiwis are less expensive than the apples" → kiwis < apples
problem.addConstraint(lambda kiwis, apples: kiwis < apples, ["kiwis", "apples"])

# 5. "The kiwis are more expensive than the mangoes" → mangoes < kiwis
problem.addConstraint(lambda mangoes, kiwis: mangoes < kiwis, ["mangoes", "kiwis"])

# Solve for the arrangement
solutions = problem.getSolutions()

# Map choice letters to fruit names
choices = {
    "A": "watermelons",
    "B": "apples",
    "C": "kiwis",
    "D": "cantaloupes",
    "E": "mangoes"
}

# Find which fruit has rank 1 (cheapest) and print the corresponding letter
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 1:
            print(letter)