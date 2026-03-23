from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
fruits = ["peaches", "watermelons", "pears", "apples", "cantaloupes"]
ranks = range(1, 6)  # 1=cheapest, 5=most expensive
problem.addVariables(fruits, ranks)

# Add constraints based on the statements
# All fruits have distinct price ranks
problem.addConstraint(AllDifferentConstraint())

# "The watermelons are the second-cheapest."
problem.addConstraint(lambda watermelons: watermelons == 2, ["watermelons"])

# "The apples are the cheapest."
problem.addConstraint(lambda apples: apples == 1, ["apples"])

# "The peaches are the most expensive."
problem.addConstraint(lambda peaches: peaches == 5, ["peaches"])

# "The pears are less expensive than the cantaloupes."
problem.addConstraint(lambda pears, cantaloupes: pears < cantaloupes, ["pears", "cantaloupes"])

# Solve the problem
solutions = problem.getSolutions()

# Check which fruit has rank 5 (most expensive) and match to choices
choices = {
    "A": "peaches",
    "B": "watermelons",
    "C": "pears",
    "D": "apples",
    "E": "cantaloupes"
}

# Since there's a unique solution, we can take the first one
solution = solutions[0]

# Find which fruit has rank 5 and print the corresponding choice letter
for letter, fruit_name in choices.items():
    if solution[fruit_name] == 5:
        print(letter)