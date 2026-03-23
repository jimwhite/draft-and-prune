from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=cheapest, 5=most expensive)
fruits = ["watermelons", "apples", "kiwis", "cantaloupes", "mangoes"]
ranks = range(1, 6)
problem.addVariables(fruits, ranks)

# Add constraints
# All fruits have different price ranks
problem.addConstraint(AllDifferentConstraint())

# The cantaloupes are the second-cheapest (rank 2)
problem.addConstraint(lambda cantaloupes: cantaloupes == 2, ["cantaloupes"])

# The mangoes are more expensive than the watermelons (watermelons < mangoes)
problem.addConstraint(lambda watermelons, mangoes: watermelons < mangoes, ["watermelons", "mangoes"])

# The kiwis are less expensive than the apples (kiwis < apples)
problem.addConstraint(lambda kiwis, apples: kiwis < apples, ["kiwis", "apples"])

# The kiwis are more expensive than the mangoes (mangoes < kiwis)
problem.addConstraint(lambda mangoes, kiwis: mangoes < kiwis, ["mangoes", "kiwis"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to fruit names
choices = {
    "A": "watermelons",
    "B": "apples",
    "C": "kiwis",
    "D": "cantaloupes",
    "E": "mangoes"
}

# Find which fruit has rank 1 (cheapest)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 1:
            print(letter)