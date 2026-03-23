from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (fruits) and domain (cost ranks: 1=cheapest, 7=most expensive)
fruits = ["watermelons", "mangoes", "kiwis", "pears", "cantaloupes", "oranges", "peaches"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add constraints based on the problem description
# 1. All fruits have different cost ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The oranges are more expensive than the peaches" → oranges > peaches
problem.addConstraint(lambda oranges, peaches: oranges > peaches, ("oranges", "peaches"))

# 3. "The cantaloupes are the fourth-most expensive" → cantaloupes == 4
problem.addConstraint(lambda cantaloupes: cantaloupes == 4, ("cantaloupes",))

# 4. "The pears are less expensive than the cantaloupes" → pears < 4
problem.addConstraint(lambda pears: pears < 4, ("pears",))

# 5. "The peaches are the second-most expensive" → peaches == 6
problem.addConstraint(lambda peaches: peaches == 6, ("peaches",))

# 6. "The mangoes are the cheapest" → mangoes == 1
problem.addConstraint(lambda mangoes: mangoes == 1, ("mangoes",))

# 7. "The kiwis are the third-cheapest" → kiwis == 3
problem.addConstraint(lambda kiwis: kiwis == 3, ("kiwis",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to fruit names for second-cheapest (rank 2)
choices = {
    'A': "watermelons",
    'B': "mangoes",
    'C': "kiwis",
    'D': "pears",
    'E': "cantaloupes",
    'F': "oranges",
    'G': "peaches"
}

# Find which fruit has rank 2 (second-cheapest)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 2:
            print(letter)