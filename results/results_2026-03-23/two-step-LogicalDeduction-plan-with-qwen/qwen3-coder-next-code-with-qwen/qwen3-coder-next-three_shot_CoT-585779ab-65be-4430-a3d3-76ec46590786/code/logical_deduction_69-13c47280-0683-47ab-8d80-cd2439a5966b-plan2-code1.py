from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
fruits = ["loquats", "peaches", "pears", "plums", "watermelons"]
ranks = range(1, 6)  # 1=cheapest, 5=most expensive
problem.addVariables(fruits, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The watermelons are the most expensive."
problem.addConstraint(lambda watermelons: watermelons == 5, ["watermelons"])

# "The peaches are more expensive than the loquats."
# More expensive means lower rank number
problem.addConstraint(lambda peaches, loquats: peaches < loquats, ["peaches", "loquats"])

# "The plums are the second-cheapest."
problem.addConstraint(lambda plums: plums == 2, ["plums"])

# "The pears are the third-most expensive."
problem.addConstraint(lambda pears: pears == 3, ["pears"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to fruit names
choices = {
    "A": "loquats",
    "B": "peaches",
    "C": "pears",
    "D": "plums",
    "E": "watermelons"
}

# Find which fruit has rank 4 (second-most expensive)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 4:
            print(letter)