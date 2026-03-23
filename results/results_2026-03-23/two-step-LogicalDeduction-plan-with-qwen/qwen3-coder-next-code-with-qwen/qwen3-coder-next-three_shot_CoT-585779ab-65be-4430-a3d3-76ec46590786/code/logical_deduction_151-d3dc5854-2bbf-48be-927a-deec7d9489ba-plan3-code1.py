from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=cheapest, 7=most expensive)
fruits = ["watermelons", "mangoes", "kiwis", "pears", "cantaloupes", "oranges", "peaches"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add all different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem description:
# 1. "The oranges are more expensive than the peaches" → peaches < oranges
problem.addConstraint(lambda peaches, oranges: peaches < oranges, ("peaches", "oranges"))

# 2. "The cantaloupes are the fourth-most expensive" → cantaloupes == 4
problem.addConstraint(lambda cantaloupes: cantaloupes == 4, ("cantaloupes",))

# 3. "The pears are less expensive than the cantaloupes" → pears < cantaloupes
problem.addConstraint(lambda pears, cantaloupes: pears < cantaloupes, ("pears", "cantaloupes"))

# 4. "The peaches are the second-most expensive" → peaches == 6
problem.addConstraint(lambda peaches: peaches == 6, ("peaches",))

# 5. "The mangoes are the cheapest" → mangoes == 1
problem.addConstraint(lambda mangoes: mangoes == 1, ("mangoes",))

# 6. "The kiwis are the third-cheapest" → kiwis == 3
problem.addConstraint(lambda kiwis: kiwis == 3, ("kiwis",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to fruits
choices = {
    "A": "watermelons",
    "B": "mangoes",
    "C": "kiwis",
    "D": "pears",
    "E": "cantaloupes",
    "F": "oranges",
    "G": "peaches"
}

# Find which fruit has rank 6 (second-most expensive)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 6:
            print(letter)