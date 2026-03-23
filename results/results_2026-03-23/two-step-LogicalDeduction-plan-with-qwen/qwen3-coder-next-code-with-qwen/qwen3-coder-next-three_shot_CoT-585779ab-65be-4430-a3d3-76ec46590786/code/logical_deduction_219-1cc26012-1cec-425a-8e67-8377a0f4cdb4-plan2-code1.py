from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=cheapest, 7=most expensive)
fruits = ["mangoes", "cantaloupes", "apples", "plums", "loquats", "watermelons", "peaches"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem description:
# 1. "The plums are more expensive than the mangoes" → plums < mangoes
problem.addConstraint(lambda plums, mangoes: plums < mangoes, ("plums", "mangoes"))

# 2. "The watermelons are more expensive than the loquats" → watermelons < loquats
problem.addConstraint(lambda watermelons, loquats: watermelons < loquats, ("watermelons", "loquats"))

# 3. "The loquats are the second-cheapest" → loquats == 2
problem.addConstraint(lambda loquats: loquats == 2, ("loquats",))

# 4. "The plums are less expensive than the peaches" → plums > peaches
problem.addConstraint(lambda plums, peaches: plums > peaches, ("plums", "peaches"))

# 5. "The mangoes are the fourth-most expensive" → mangoes == 4
problem.addConstraint(lambda mangoes: mangoes == 4, ("mangoes",))

# 6. "The peaches are less expensive than the cantaloupes" → peaches > cantaloupes
problem.addConstraint(lambda peaches, cantaloupes: peaches > cantaloupes, ("peaches", "cantaloupes"))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to fruit names
choices = {
    "A": "mangoes",
    "B": "cantaloupes",
    "C": "apples",
    "D": "plums",
    "E": "loquats",
    "F": "watermelons",
    "G": "peaches"
}

# Find the fruit with rank 7 (most expensive) and print corresponding choice letter
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 7:
            print(letter)