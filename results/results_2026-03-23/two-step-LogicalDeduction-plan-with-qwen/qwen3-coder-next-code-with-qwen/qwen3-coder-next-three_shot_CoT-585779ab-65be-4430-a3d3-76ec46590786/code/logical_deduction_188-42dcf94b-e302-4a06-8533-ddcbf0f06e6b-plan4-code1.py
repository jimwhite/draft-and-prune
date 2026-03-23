from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (the seven fruits) and domain (price ranks 1-7, where 1=cheapest, 7=most expensive)
fruits = ["mangoes", "watermelons", "peaches", "kiwis", "oranges", "cantaloupes", "plums"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add constraints based on the problem description
# 1. All fruits have different price ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The watermelons are the cheapest."
problem.addConstraint(lambda watermelons: watermelons == 1, ["watermelons"])

# 3. "The kiwis are the third-cheapest."
problem.addConstraint(lambda kiwis: kiwis == 3, ["kiwis"])

# 4. "The cantaloupes are the second-most expensive."
problem.addConstraint(lambda cantaloupes: cantaloupes == 6, ["cantaloupes"])

# 5. "The oranges are more expensive than the cantaloupes."
problem.addConstraint(lambda cantaloupes, oranges: cantaloupes < oranges, ["cantaloupes", "oranges"])

# 6. "The peaches are more expensive than the mangoes."
problem.addConstraint(lambda mangoes, peaches: mangoes < peaches, ["mangoes", "peaches"])

# 7. "The peaches are less expensive than the plums."
problem.addConstraint(lambda peaches, plums: peaches < plums, ["peaches", "plums"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to fruit names
choices = {
    "A": "mangoes",
    "B": "watermelons",
    "C": "peaches",
    "D": "kiwis",
    "E": "oranges",
    "F": "cantaloupes",
    "G": "plums"
}

# Find which fruit has rank 2 (second-cheapest)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 2:
            print(letter)