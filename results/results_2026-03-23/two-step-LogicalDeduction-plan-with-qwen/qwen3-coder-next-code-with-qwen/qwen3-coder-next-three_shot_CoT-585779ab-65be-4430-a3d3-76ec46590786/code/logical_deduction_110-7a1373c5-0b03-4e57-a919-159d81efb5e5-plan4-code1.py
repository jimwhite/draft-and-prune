from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define the seven fruits as variables
fruits = ["cantaloupes", "plums", "mangoes", "apples", "loquats", "pears", "peaches"]

# Define domain: 1 = cheapest, 7 = most expensive
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add constraint that all fruits have different ranks
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem description:
# "The apples are less expensive than the cantaloupes" → apples < cantaloupes
problem.addConstraint(lambda apples, cantaloupes: apples < cantaloupes, ("apples", "cantaloupes"))

# "The apples are more expensive than the peaches" → peaches < apples
problem.addConstraint(lambda peaches, apples: peaches < apples, ("peaches", "apples"))

# "The mangoes are the fourth-most expensive" → rank = 4
problem.addConstraint(lambda mangoes: mangoes == 4, ("mangoes",))

# "The peaches are more expensive than the plums" → plums < peaches
problem.addConstraint(lambda plums, peaches: plums < peaches, ("plums", "peaches"))

# "The pears are the third-most expensive" → rank = 5 (since 7=1st,6=2nd,5=3rd)
problem.addConstraint(lambda pears: pears == 5, ("pears",))

# "The loquats are the third-cheapest" → rank = 3
problem.addConstraint(lambda loquats: loquats == 3, ("loquats",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to fruit names
choices = {
    "A": "cantaloupes",
    "B": "plums",
    "C": "mangoes",
    "D": "apples",
    "E": "loquats",
    "F": "pears",
    "G": "peaches"
}

# Find which fruit has rank 6 (second-most expensive)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 6:
            print(letter)