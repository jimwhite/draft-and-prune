from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (the seven fruits) and domain (price ranks 1 to 7, where 1=cheapest, 7=most expensive)
fruits = ["watermelons", "oranges", "mangoes", "cantaloupes", "kiwis", "pears", "peaches"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add constraints based on the problem description
# 1. All fruits must have different price ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The pears are the second-cheapest" → pears = 2
problem.addConstraint(lambda pears: pears == 2, ["pears"])

# 3. "The peaches are more expensive than the cantaloupes" → cantaloupes < peaches
problem.addConstraint(lambda cantaloupes, peaches: cantaloupes < peaches, ["cantaloupes", "peaches"])

# 4. "The peaches are less expensive than the mangoes" → peaches < mangoes
problem.addConstraint(lambda peaches, mangoes: peaches < mangoes, ["peaches", "mangoes"])

# 5. "The cantaloupes are more expensive than the kiwis" → kiwis < cantaloupes
problem.addConstraint(lambda kiwis, cantaloupes: kiwis < cantaloupes, ["kiwis", "cantaloupes"])

# 6. "The oranges are the fourth-most expensive" → oranges = 4
problem.addConstraint(lambda oranges: oranges == 4, ["oranges"])

# 7. "The watermelons are the second-most expensive" → watermelons = 6 (since most expensive is 7)
problem.addConstraint(lambda watermelons: watermelons == 6, ["watermelons"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to fruit names
choices = {
    "A": "watermelons",
    "B": "oranges",
    "C": "mangoes",
    "D": "cantaloupes",
    "E": "kiwis",
    "F": "pears",
    "G": "peaches"
}

# Find which fruit has rank 4 (fourth-most expensive)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 4:
            print(letter)