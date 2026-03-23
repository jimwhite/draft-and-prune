from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=cheapest, 5=most expensive)
fruits = ["mangoes", "cantaloupes", "plums", "oranges", "watermelons"]
ranks = range(1, 6)
problem.addVariables(fruits, ranks)

# Add constraints based on the problem description
# 1. All fruits have different price ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The oranges are more expensive than the watermelons" → oranges > watermelons
problem.addConstraint(lambda oranges, watermelons: oranges > watermelons, ("oranges", "watermelons"))

# 3. "The watermelons are the second-cheapest" → watermelons == 2
problem.addConstraint(lambda watermelons: watermelons == 2, ("watermelons",))

# 4. "The plums are less expensive than the cantaloupes" → plums < cantaloupes
problem.addConstraint(lambda plums, cantaloupes: plums < cantaloupes, ("plums", "cantaloupes"))

# 5. "The plums are the second-most expensive" → plums == 4
problem.addConstraint(lambda plums: plums == 4, ("plums",))

# Solve the problem
solutions = problem.getSolutions()

# Map choices to fruits
choices = {
    "A": "mangoes",
    "B": "cantaloupes",
    "C": "plums",
    "D": "oranges",
    "E": "watermelons"
}

# Find which fruit has rank 4 (second-most expensive) and print the corresponding choice letter
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 4:
            print(letter)