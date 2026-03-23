from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (positions 1=cheapest, 7=most expensive)
fruits = ["watermelons", "oranges", "mangoes", "cantaloupes", "kiwis", "pears", "peaches"]
positions = range(1, 8)
problem.addVariables(fruits, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem statements:
# - pears are second-cheapest → position 2
problem.addConstraint(lambda pears: pears == 2, ["pears"])
# - oranges are fourth-most expensive → position 4 (since most expensive=7, second=6, third=5, fourth=4)
problem.addConstraint(lambda oranges: oranges == 4, ["oranges"])
# - watermelons are second-most expensive → position 6
problem.addConstraint(lambda watermelons: watermelons == 6, ["watermelons"])
# - peaches are more expensive than cantaloupes → peaches > cantaloupes
problem.addConstraint(lambda peaches, cantaloupes: peaches > cantaloupes, ["peaches", "cantaloupes"])
# - peaches are less expensive than mangoes → mangoes > peaches
problem.addConstraint(lambda mangoes, peaches: mangoes > peaches, ["mangoes", "peaches"])
# - cantaloupes are more expensive than kiwis → cantaloupes > kiwis
problem.addConstraint(lambda cantaloupes, kiwis: cantaloupes > kiwis, ["cantaloupes", "kiwis"])

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

# Find which fruit is at position 4 (fourth-most expensive)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 4:
            print(letter)