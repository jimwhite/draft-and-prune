from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
fruits = ["plums", "kiwis", "cantaloupes", "pears", "watermelons", "apples", "loquats"]
ranks = range(1, 8)  # 1=cheapest, 7=most expensive
problem.addVariables(fruits, ranks)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem statements
# "The watermelons are the second-most expensive" -> rank 6 (since 7 is most expensive)
problem.addConstraint(lambda watermelons: watermelons == 6, ["watermelons"])

# "The loquats are the third-cheapest" -> rank 3 (since 1=cheapest, 2=second-cheapest)
problem.addConstraint(lambda loquats: loquats == 3, ["loquats"])

# "The plums are the cheapest" -> rank 1
problem.addConstraint(lambda plums: plums == 1, ["plums"])

# "The watermelons are more expensive than the cantaloupes" -> cantaloupes < watermelons
problem.addConstraint(lambda cantaloupes, watermelons: cantaloupes < watermelons, ["cantaloupes", "watermelons"])

# "The apples are less expensive than the cantaloupes" -> apples < cantaloupes
problem.addConstraint(lambda apples, cantaloupes: apples < cantaloupes, ["apples", "cantaloupes"])

# "The loquats are less expensive than the kiwis" -> loquats < kiwis
problem.addConstraint(lambda loquats, kiwis: loquats < kiwis, ["loquats", "kiwis"])

# "The apples are more expensive than the loquats" -> loquats < apples
problem.addConstraint(lambda loquats, apples: loquats < apples, ["loquats", "apples"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to fruit names
choices = {
    "A": "plums",
    "B": "kiwis",
    "C": "cantaloupes",
    "D": "pears",
    "E": "watermelons",
    "F": "apples",
    "G": "loquats"
}

# Find which fruit has rank 4 (fourth-most expensive)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 4:
            print(letter)