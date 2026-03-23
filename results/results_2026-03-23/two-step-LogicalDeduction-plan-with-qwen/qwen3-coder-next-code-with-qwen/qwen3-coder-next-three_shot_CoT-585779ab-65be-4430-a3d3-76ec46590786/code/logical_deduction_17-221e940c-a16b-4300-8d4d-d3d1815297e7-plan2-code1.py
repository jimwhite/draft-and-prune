from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
fruits = ["watermelons", "apples", "mangoes", "pears", "cantaloupes"]
ranks = range(1, 6)  # 1=cheapest, 5=most expensive
problem.addVariables(fruits, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The watermelons are more expensive than the cantaloupes"
problem.addConstraint(lambda watermelons, cantaloupes: watermelons > cantaloupes, ("watermelons", "cantaloupes"))

# "The mangoes are less expensive than the pears"
problem.addConstraint(lambda mangoes, pears: mangoes < pears, ("mangoes", "pears"))

# "The apples are the second-cheapest"
problem.addConstraint(lambda apples: apples == 2, ("apples",))

# "The watermelons are less expensive than the mangoes"
problem.addConstraint(lambda watermelons, mangoes: watermelons < mangoes, ("watermelons", "mangoes"))

# Solve the problem
solutions = problem.getSolutions()

# Map choices to fruits
choices = {
    "A": "watermelons",
    "B": "apples",
    "C": "mangoes",
    "D": "pears",
    "E": "cantaloupes"
}

# Find the cheapest fruit (rank 1) and print corresponding choice letter
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 1:
            print(letter)