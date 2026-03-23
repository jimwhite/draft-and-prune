from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=cheapest, 7=most expensive)
fruits = ["cantaloupes", "plums", "mangoes", "apples", "loquats", "pears", "peaches"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem description:
# 1. "The apples are less expensive than the cantaloupes" → apples < cantaloupes
problem.addConstraint(lambda apples, cantaloupes: apples < cantaloupes, ("apples", "cantaloupes"))

# 2. "The apples are more expensive than the peaches" → apples > peaches
problem.addConstraint(lambda apples, peaches: apples > peaches, ("apples", "peaches"))

# 3. "The mangoes are the fourth-most expensive" → mangoes == 4
problem.addConstraint(lambda mangoes: mangoes == 4, ["mangoes"])

# 4. "The peaches are more expensive than the plums" → peaches > plums
problem.addConstraint(lambda peaches, plums: peaches > plums, ("peaches", "plums"))

# 5. "The pears are the third-most expensive" → pears == 5 (since 7=most expensive, 6=second-most, 5=third-most)
problem.addConstraint(lambda pears: pears == 5, ["pears"])

# 6. "The loquats are the third-cheapest" → loquats == 3 (since 1=cheapest, 2=second-cheapest, 3=third-cheapest)
problem.addConstraint(lambda loquats: loquats == 3, ["loquats"])

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

# Find which fruit has rank 4 (fourth-most expensive)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 4:
            print(letter)