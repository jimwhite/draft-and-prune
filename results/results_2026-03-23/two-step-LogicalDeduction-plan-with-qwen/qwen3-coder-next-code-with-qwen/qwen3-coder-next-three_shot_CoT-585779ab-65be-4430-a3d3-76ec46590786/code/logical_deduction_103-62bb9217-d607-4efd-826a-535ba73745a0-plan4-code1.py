from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=cheapest, 7=most expensive)
fruits = ["plums", "kiwis", "cantaloupes", "pears", "watermelons", "apples", "loquats"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add all different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem statements:
# 1. "The watermelons are more expensive than the cantaloupes" → watermelons > cantaloupes
problem.addConstraint(lambda watermelons, cantaloupes: watermelons > cantaloupes, ("watermelons", "cantaloupes"))

# 2. "The apples are less expensive than the cantaloupes" → apples < cantaloupes
problem.addConstraint(lambda apples, cantaloupes: apples < cantaloupes, ("apples", "cantaloupes"))

# 3. "The watermelons are the second-most expensive" → watermelons == 6
problem.addConstraint(lambda watermelons: watermelons == 6, ("watermelons",))

# 4. "The loquats are less expensive than the kiwis" → loquats < kiwis
problem.addConstraint(lambda loquats, kiwis: loquats < kiwis, ("loquats", "kiwis"))

# 5. "The apples are more expensive than the loquats" → apples > loquats
problem.addConstraint(lambda apples, loquats: apples > loquats, ("apples", "loquats"))

# 6. "The loquats are the third-cheapest" → loquats == 3
problem.addConstraint(lambda loquats: loquats == 3, ("loquats",))

# 7. "The plums are the cheapest" → plums == 1
problem.addConstraint(lambda plums: plums == 1, ("plums",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to fruit names as given in the choices
choices = {
    "A": "plums",
    "B": "kiwis",
    "C": "cantaloupes",
    "D": "pears",
    "E": "watermelons",
    "F": "apples",
    "G": "loquats"
}

# Find the fruit with rank 5 (third-most-expensive: positions are 7=most, 6=second-most, 5=third-most)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 5:
            print(letter)