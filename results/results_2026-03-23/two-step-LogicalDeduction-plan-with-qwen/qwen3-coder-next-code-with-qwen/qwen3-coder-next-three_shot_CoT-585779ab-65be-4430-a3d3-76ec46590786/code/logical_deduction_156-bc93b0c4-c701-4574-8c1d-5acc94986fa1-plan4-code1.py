from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=cheapest, 7=most expensive)
fruits = ["watermelons", "oranges", "mangoes", "cantaloupes", "kiwis", "pears", "peaches"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add constraints
# All fruits have distinct price ranks
problem.addConstraint(AllDifferentConstraint())

# The pears are the second-cheapest → rank 2
problem.addConstraint(lambda pears: pears == 2, ["pears"])

# The oranges are the fourth-most expensive → rank 4
problem.addConstraint(lambda oranges: oranges == 4, ["oranges"])

# The watermelons are the second-most expensive → rank 6
problem.addConstraint(lambda watermelons: watermelons == 6, ["watermelons"])

# The peaches are more expensive than the cantaloupes → cantaloupes < peaches
problem.addConstraint(lambda cantaloupes, peaches: cantaloupes < peaches, ["cantaloupes", "peaches"])

# The peaches are less expensive than the mangoes → peaches < mangoes
problem.addConstraint(lambda peaches, mangoes: peaches < mangoes, ["peaches", "mangoes"])

# The cantaloupes are more expensive than the kiwis → kiwis < cantaloupes
problem.addConstraint(lambda kiwis, cantaloupes: kiwis < cantaloupes, ["kiwis", "cantaloupes"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to fruit names
choices = {
    'A': 'watermelons',
    'B': 'oranges',
    'C': 'mangoes',
    'D': 'cantaloupes',
    'E': 'kiwis',
    'F': 'pears',
    'G': 'peaches'
}

# Find which fruit has rank 4 (fourth-most expensive)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 4:
            print(letter)