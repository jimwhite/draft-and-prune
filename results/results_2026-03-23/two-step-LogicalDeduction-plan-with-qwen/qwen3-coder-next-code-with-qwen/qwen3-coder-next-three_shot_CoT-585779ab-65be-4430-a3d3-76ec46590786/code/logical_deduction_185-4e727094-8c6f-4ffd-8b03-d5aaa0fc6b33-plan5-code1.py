from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (the seven fruits) and domain (price ranks 1 to 7, where 1=cheapest, 7=most expensive)
fruits = ["plums", "kiwis", "cantaloupes", "pears", "watermelons", "apples", "loquats"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add constraints based on the problem description
# 1. All fruits must have different price ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The watermelons are the second-most expensive" → rank 6 (since 7 is most expensive)
problem.addConstraint(lambda watermelons: watermelons == 6, ["watermelons"])

# 3. "The loquats are the third-cheapest" → rank 3
problem.addConstraint(lambda loquats: loquats == 3, ["loquats"])

# 4. "The plums are the cheapest" → rank 1
problem.addConstraint(lambda plums: plums == 1, ["plums"])

# 5. "The watermelons are more expensive than the cantaloupes" → cantaloupes < watermelons (cantaloupes < 6)
problem.addConstraint(lambda cantaloupes, watermelons: cantaloupes < watermelons, ["cantaloupes", "watermelons"])

# 6. "The apples are less expensive than the cantaloupes" → apples < cantaloupes
problem.addConstraint(lambda apples, cantaloupes: apples < cantaloupes, ["apples", "cantaloupes"])

# 7. "The loquats are less expensive than the kiwis" → loquats < kiwis (3 < kiwis)
problem.addConstraint(lambda loquats, kiwis: loquats < kiwis, ["loquats", "kiwis"])

# 8. "The apples are more expensive than the loquats" → apples > loquats (apples > 3)
problem.addConstraint(lambda apples, loquats: apples > loquats, ["apples", "loquats"])

# Solve the problem
solutions = problem.getSolutions()

# The question asks which fruit is the fourth-most expensive (rank 4)
choices = {
    "A": "plums",
    "B": "kiwis",
    "C": "cantaloupes",
    "D": "pears",
    "E": "watermelons",
    "F": "apples",
    "G": "loquats"
}

# Find the fruit with rank 4 and print its corresponding choice letter
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 4:
            print(letter)