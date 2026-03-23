from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define the seven fruits as variables
fruits = ["mangoes", "cantaloupes", "apples", "plums", "loquats", "watermelons", "peaches"]

# Define the domain: positions 1 to 7, where 1 = cheapest and 7 = most expensive
positions = range(1, 8)
problem.addVariables(fruits, positions)

# Add constraint that all fruits have distinct price ranks
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem statements:
# "The plums are more expensive than the mangoes" → plums > mangoes
problem.addConstraint(lambda plums, mangoes: plums > mangoes, ("plums", "mangoes"))

# "The watermelons are more expensive than the loquats" → watermelons > loquats
problem.addConstraint(lambda watermelons, loquats: watermelons > loquats, ("watermelons", "loquats"))

# "The loquats are the second-cheapest" → loquats == 2
problem.addConstraint(lambda loquats: loquats == 2, ("loquats",))

# "The plums are less expensive than the peaches" → plums < peaches
problem.addConstraint(lambda plums, peaches: plums < peaches, ("plums", "peaches"))

# "The mangoes are the fourth-most expensive" → mangoes == 4
problem.addConstraint(lambda mangoes: mangoes == 4, ("mangoes",))

# "The peaches are less expensive than the cantaloupes" → peaches < cantaloupes
problem.addConstraint(lambda peaches, cantaloupes: peaches < cantaloupes, ("peaches", "cantaloupes"))

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

# Find which fruit has rank 1 (cheapest)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 1:
            print(letter)