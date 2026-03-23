from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
fruits = ["mangoes", "cantaloupes", "plums", "oranges", "watermelons"]
ranks = range(1, 6)  # 1=cheapest, 5=most expensive
problem.addVariables(fruits, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The oranges are more expensive than the watermelons"
problem.addConstraint(lambda oranges, watermelons: oranges > watermelons, ("oranges", "watermelons"))

# "The watermelons are the second-cheapest"
problem.addConstraint(lambda watermelons: watermelons == 2, ("watermelons",))

# "The plums are less expensive than the cantaloupes"
problem.addConstraint(lambda plums, cantaloupes: plums < cantaloupes, ("plums", "cantaloupes"))

# "The plums are the second-most expensive"
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

# Find which fruit is second-most expensive (rank 4)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 4:
            print(letter)