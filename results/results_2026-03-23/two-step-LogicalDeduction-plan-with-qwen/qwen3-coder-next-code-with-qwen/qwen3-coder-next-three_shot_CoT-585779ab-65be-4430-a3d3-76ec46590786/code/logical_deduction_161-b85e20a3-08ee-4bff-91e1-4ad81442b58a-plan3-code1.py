from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=cheapest, 7=most expensive)
fruits = ["kiwis", "cantaloupes", "oranges", "loquats", "pears", "watermelons", "peaches"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem statements:
# 1. "The loquats are less expensive than the peaches" → loquats < peaches
problem.addConstraint(lambda loquats, peaches: loquats < peaches, ("loquats", "peaches"))

# 2. "The pears are the third-cheapest" → pears == 3
problem.addConstraint(lambda pears: pears == 3, ("pears",))

# 3. "The oranges are less expensive than the cantaloupes" → oranges < cantaloupes
problem.addConstraint(lambda oranges, cantaloupes: oranges < cantaloupes, ("oranges", "cantaloupes"))

# 4. "The loquats are more expensive than the watermelons" → watermelons < loquats
problem.addConstraint(lambda watermelons, loquats: watermelons < loquats, ("watermelons", "loquats"))

# 5. "The peaches are less expensive than the oranges" → peaches < oranges
problem.addConstraint(lambda peaches, oranges: peaches < oranges, ("peaches", "oranges"))

# 6. "The kiwis are the second-most expensive" → kiwis == 6 (since most expensive is rank 7)
problem.addConstraint(lambda kiwis: kiwis == 6, ("kiwis",))

# Solve the problem
solutions = problem.getSolutions()

# Map choices to fruit names (A-G)
choices = {
    "A": "kiwis",
    "B": "cantaloupes",
    "C": "oranges",
    "D": "loquats",
    "E": "pears",
    "F": "watermelons",
    "G": "peaches"
}

# Find the fruit with rank 5 (third-most expensive in a list of 7)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 5:
            print(letter)