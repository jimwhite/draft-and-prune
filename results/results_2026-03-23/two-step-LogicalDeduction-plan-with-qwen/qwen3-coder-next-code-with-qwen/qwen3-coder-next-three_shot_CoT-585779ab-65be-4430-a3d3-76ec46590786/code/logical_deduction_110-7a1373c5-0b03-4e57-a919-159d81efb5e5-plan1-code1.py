from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=cheapest, 7=most expensive)
fruits = ["cantaloupes", "plums", "mangoes", "apples", "loquats", "pears", "peaches"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# 1. "The apples are less expensive than the cantaloupes" → apples < cantaloupes
problem.addConstraint(lambda apples, cantaloupes: apples < cantaloupes, ("apples", "cantaloupes"))

# 2. "The apples are more expensive than the peaches" → peaches < apples
problem.addConstraint(lambda peaches, apples: peaches < apples, ("peaches", "apples"))

# 3. "The mangoes are the fourth-most expensive" → mangoes == 4
problem.addConstraint(lambda mangoes: mangoes == 4, ("mangoes",))

# 4. "The peaches are more expensive than the plums" → plums < peaches
problem.addConstraint(lambda plums, peaches: plums < peaches, ("plums", "peaches"))

# 5. "The pears are the third-most expensive" → pears == 5
problem.addConstraint(lambda pears: pears == 5, ("pears",))

# 6. "The loquats are the third-cheapest" → loquats == 3
problem.addConstraint(lambda loquats: loquats == 3, ("loquats",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to fruit names
choices = {
    "A": "cantaloupes",
    "B": "plums",
    "C": "mangoes",
    "D": "apples",
    "E": "loquats",
    "F": "pears",
    "G": "peaches"
}

# Find which fruit has rank 6 (second-most expensive)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 6:
            print(letter)