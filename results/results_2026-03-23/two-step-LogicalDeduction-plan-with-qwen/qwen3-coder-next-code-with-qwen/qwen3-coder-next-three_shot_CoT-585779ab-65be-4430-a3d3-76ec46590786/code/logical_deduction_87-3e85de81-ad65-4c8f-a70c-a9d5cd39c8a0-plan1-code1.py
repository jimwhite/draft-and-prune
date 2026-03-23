from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
fruits = ["loquats", "pears", "watermelons", "kiwis", "plums"]
ranks = range(1, 6)  # 1 = most expensive, 5 = least expensive
problem.addVariables(fruits, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The loquats are the third-most expensive"
problem.addConstraint(lambda loquats: loquats == 3, ["loquats"])

# "The loquats are more expensive than the watermelons"
problem.addConstraint(lambda loquats, watermelons: loquats < watermelons, ["loquats", "watermelons"])

# "The plums are less expensive than the watermelons"
problem.addConstraint(lambda plums, watermelons: plums > watermelons, ["plums", "watermelons"])

# "The kiwis are more expensive than the pears"
problem.addConstraint(lambda kiwis, pears: kiwis < pears, ["kiwis", "pears"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to fruit names
choices = {
    "A": "loquats",
    "B": "pears",
    "C": "watermelons",
    "D": "kiwis",
    "E": "plums"
}

# Find which fruit has rank 2 (second-most expensive)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 2:
            print(letter)