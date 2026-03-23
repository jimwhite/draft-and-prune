from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (ranks: 1=cheapest, 7=most expensive)
fruits = ["plums", "kiwis", "cantaloupes", "pears", "watermelons", "apples", "loquats"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add AllDifferent constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem statements
# "The watermelons are the second-most expensive" → rank 6 (since most expensive = 7)
problem.addConstraint(lambda watermelons: watermelons == 6, ["watermelons"])

# "The plums are the cheapest" → rank 1
problem.addConstraint(lambda plums: plums == 1, ["plums"])

# "The loquats are the third-cheapest" → rank 3
problem.addConstraint(lambda loquats: loquats == 3, ["loquats"])

# "The watermelons are more expensive than the cantaloupes" → watermelons > cantaloupes
problem.addConstraint(lambda watermelons, cantaloupes: watermelons > cantaloupes, ["watermelons", "cantaloupes"])

# "The apples are less expensive than the cantaloupes" → apples < cantaloupes
problem.addConstraint(lambda apples, cantaloupes: apples < cantaloupes, ["apples", "cantaloupes"])

# "The loquats are less expensive than the kiwis" → loquats < kiwis
problem.addConstraint(lambda loquats, kiwis: loquats < kiwis, ["loquats", "kiwis"])

# "The apples are more expensive than the loquats" → apples > loquats
problem.addConstraint(lambda apples, loquats: apples > loquats, ["apples", "loquats"])

# Solve the problem
solutions = problem.getSolutions()

# Find which fruit has rank 4 (fourth-most expensive)
for solution in solutions:
    for fruit, rank in solution.items():
        if rank == 4:
            # Map to answer choices
            fruit_to_choice = {
                "plums": "A",
                "kiwis": "B",
                "cantaloupes": "C",
                "pears": "D",
                "watermelons": "E",
                "apples": "F",
                "loquats": "G"
            }
            print(fruit_to_choice[fruit])