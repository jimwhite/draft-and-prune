from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
fruits = ["mangoes", "cantaloupes", "apples", "plums", "loquats", "watermelons", "peaches"]
ranks = range(1, 8)  # 1=cheapest, 7=most expensive
problem.addVariables(fruits, ranks)

# Add AllDifferent constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# "The plums are more expensive than the mangoes" → mangoes < plums (mangoes cheaper, so smaller rank)
problem.addConstraint(lambda mangoes, plums: mangoes < plums, ("mangoes", "plums"))

# "The watermelons are more expensive than the loquats" → loquats < watermelons
problem.addConstraint(lambda loquats, watermelons: loquats < watermelons, ("loquats", "watermelons"))

# "The loquats are the second-cheapest" → loquats = 2
problem.addConstraint(lambda loquats: loquats == 2, ("loquats",))

# "The plums are less expensive than the peaches" → plums < peaches
problem.addConstraint(lambda plums, peaches: plums < peaches, ("plums", "peaches"))

# "The mangoes are the fourth-most expensive" → mangoes = 4
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

# Find the fruit with rank 7 (most expensive)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 7:
            print(letter)