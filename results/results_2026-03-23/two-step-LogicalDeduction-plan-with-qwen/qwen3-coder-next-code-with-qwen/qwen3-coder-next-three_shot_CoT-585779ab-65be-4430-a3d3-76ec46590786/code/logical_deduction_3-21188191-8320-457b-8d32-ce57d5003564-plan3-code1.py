from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
fruits = ["watermelons", "plums", "apples", "peaches", "kiwis"]
ranks = range(1, 6)
problem.addVariables(fruits, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The apples are less expensive than the peaches"
problem.addConstraint(lambda apples, peaches: apples < peaches, ["apples", "peaches"])

# "The plums are the cheapest"
problem.addConstraint(lambda plums: plums == 1, ["plums"])

# "The kiwis are the second-cheapest"
problem.addConstraint(lambda kiwis: kiwis == 2, ["kiwis"])

# "The watermelons are more expensive than the peaches"
problem.addConstraint(lambda peaches, watermelons: peaches < watermelons, ["peaches", "watermelons"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to fruits
choices = {
    "A": "watermelons",
    "B": "plums",
    "C": "apples",
    "D": "peaches",
    "E": "kiwis"
}

# Find the fruit with rank 5 (most expensive)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 5:
            print(letter)