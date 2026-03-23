from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (price ranks 1=cheapest to 7=most expensive)
fruits = ["mangoes", "watermelons", "peaches", "kiwis", "oranges", "cantaloupes", "plums"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add constraints
# All fruits have different price ranks
problem.addConstraint(AllDifferentConstraint())

# "The watermelons are the cheapest."
problem.addConstraint(lambda watermelons: watermelons == 1, ["watermelons"])

# "The peaches are more expensive than the mangoes."
problem.addConstraint(lambda peaches, mangoes: peaches > mangoes, ["peaches", "mangoes"])

# "The cantaloupes are the second-most expensive."
problem.addConstraint(lambda cantaloupes: cantaloupes == 6, ["cantaloupes"])

# "The oranges are more expensive than the cantaloupes."
problem.addConstraint(lambda oranges, cantaloupes: oranges > cantaloupes, ["oranges", "cantaloupes"])

# "The peaches are less expensive than the plums."
problem.addConstraint(lambda peaches, plums: peaches < plums, ["peaches", "plums"])

# "The kiwis are the third-cheapest."
problem.addConstraint(lambda kiwis: kiwis == 3, ["kiwis"])

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

# Find which fruit has rank 1 (cheapest)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 1:
            print(letter)