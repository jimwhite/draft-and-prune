from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (the seven fruits) and domain (price ranks 1 to 7)
fruits = ["plums", "kiwis", "cantaloupes", "pears", "watermelons", "apples", "loquats"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add constraints based on the puzzle statements
# 1. All fruits must have different price ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The watermelons are more expensive than the cantaloupes"
problem.addConstraint(lambda watermelons, cantaloupes: watermelons > cantaloupes, ("watermelons", "cantaloupes"))

# 3. "The apples are less expensive than the cantaloupes"
problem.addConstraint(lambda apples, cantaloupes: apples < cantaloupes, ("apples", "cantaloupes"))

# 4. "The watermelons are the second-most expensive" (rank 6, since most expensive = 7)
problem.addConstraint(lambda watermelons: watermelons == 6, ("watermelons",))

# 5. "The loquats are less expensive than the kiwis"
problem.addConstraint(lambda loquats, kiwis: loquats < kiwis, ("loquats", "kiwis"))

# 6. "The apples are more expensive than the loquats"
problem.addConstraint(lambda apples, loquats: apples > loquats, ("apples", "loquats"))

# 7. "The loquats are the third-cheapest" (rank 3)
problem.addConstraint(lambda loquats: loquats == 3, ("loquats",))

# 8. "The plums are the cheapest" (rank 1)
problem.addConstraint(lambda plums: plums == 1, ("plums",))

# Solve for the arrangement
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