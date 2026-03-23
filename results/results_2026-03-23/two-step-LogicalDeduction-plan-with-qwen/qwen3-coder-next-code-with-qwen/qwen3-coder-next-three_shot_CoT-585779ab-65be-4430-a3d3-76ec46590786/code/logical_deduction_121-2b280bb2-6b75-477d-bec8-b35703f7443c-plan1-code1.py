from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=cheapest, 7=most expensive)
fruits = ["loquats", "peaches", "watermelons", "plums", "kiwis", "mangoes", "pears"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add all different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem description:
# 1. "The pears are more expensive than the kiwis" → pears > kiwis
problem.addConstraint(lambda p, k: p > k, ("pears", "kiwis"))

# 2. "The watermelons are less expensive than the peaches" → watermelons < peaches
problem.addConstraint(lambda w, p: w < p, ("watermelons", "peaches"))

# 3. "The mangoes are the third-cheapest" → mangoes == 3
problem.addConstraint(lambda m: m == 3, ("mangoes",))

# 4. "The watermelons are the third-most expensive" → rank = 5 (since 7=most, 6=second most, 5=third most)
problem.addConstraint(lambda w: w == 5, ("watermelons",))

# 5. "The plums are the second-most expensive" → rank = 6
problem.addConstraint(lambda pl: pl == 6, ("plums",))

# 6. "The loquats are the second-cheapest" → rank = 2
problem.addConstraint(lambda l: l == 2, ("loquats",))

# Solve the problem
solutions = problem.getSolutions()

# Map choices to fruits
choices = {
    "A": "loquats",
    "B": "peaches",
    "C": "watermelons",
    "D": "plums",
    "E": "kiwis",
    "F": "mangoes",
    "G": "pears"
}

# Find which fruit has rank 3 (third-cheapest)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 3:
            print(letter)