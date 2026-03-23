from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (expense ranks 1-7, where 1=cheapest, 7=most expensive)
fruits = ["mangoes", "cantaloupes", "apples", "plums", "loquats", "watermelons", "peaches"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add AllDifferentConstraint to ensure each fruit has a unique rank
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem statements:
# 1. "The plums are more expensive than the mangoes" → plums rank < mangoes rank
problem.addConstraint(lambda plums, mangoes: plums < mangoes, ("plums", "mangoes"))

# 2. "The watermelons are more expensive than the loquats" → watermelons rank < loquats rank
problem.addConstraint(lambda watermelons, loquats: watermelons < loquats, ("watermelons", "loquats"))

# 3. "The loquats are the second-cheapest" → loquats rank = 2
problem.addConstraint(lambda loquats: loquats == 2, ("loquats",))

# 4. "The plums are less expensive than the peaches" → peaches rank < plums rank
problem.addConstraint(lambda peaches, plums: peaches < plums, ("peaches", "plums"))

# 5. "The mangoes are the fourth-most expensive" → mangoes rank = 4
problem.addConstraint(lambda mangoes: mangoes == 4, ("mangoes",))

# 6. "The peaches are less expensive than the cantaloupes" → cantaloupes rank < peaches rank
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

# Find the fruit with rank 7 (most expensive) and output corresponding choice letter
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 7:
            print(letter)