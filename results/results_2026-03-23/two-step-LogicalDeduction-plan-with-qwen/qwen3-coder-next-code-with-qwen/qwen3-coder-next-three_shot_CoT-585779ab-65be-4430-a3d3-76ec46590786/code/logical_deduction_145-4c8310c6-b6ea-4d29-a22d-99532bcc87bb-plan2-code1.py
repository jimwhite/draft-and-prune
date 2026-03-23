from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (the seven fruits) and domain (price ranks 1 to 7, where 1=cheapest)
fruits = ["mangoes", "cantaloupes", "apples", "plums", "loquats", "watermelons", "peaches"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add constraints based on the problem description
# 1. All fruits have distinct price ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The plums are more expensive than the mangoes" → plums rank < mangoes rank
problem.addConstraint(lambda plums, mangoes: plums < mangoes, ("plums", "mangoes"))

# 3. "The watermelons are more expensive than the loquats" → watermelons rank < loquats rank
problem.addConstraint(lambda watermelons, loquats: watermelons < loquats, ("watermelons", "loquats"))

# 4. "The loquats are the second-cheapest" → loquats rank == 2
problem.addConstraint(lambda loquats: loquats == 2, ("loquats",))

# 5. "The plums are less expensive than the peaches" → peaches rank < plums rank
problem.addConstraint(lambda peaches, plums: peaches < plums, ("peaches", "plums"))

# 6. "The mangoes are the fourth-most expensive" → mangoes rank == 4
problem.addConstraint(lambda mangoes: mangoes == 4, ("mangoes",))

# 7. "The peaches are less expensive than the cantaloupes" → cantaloupes rank < peaches rank
problem.addConstraint(lambda cantaloupes, peaches: cantaloupes < peaches, ("cantaloupes", "peaches"))

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

# Find the cheapest fruit (rank 1) and print corresponding choice letter
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 1:
            print(letter)