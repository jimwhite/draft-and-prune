from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=cheapest, 5=most expensive)
fruits = ["loquats", "peaches", "pears", "plums", "watermelons"]
ranks = range(1, 6)
problem.addVariables(fruits, ranks)

# Add constraints
# All fruits have different price ranks
problem.addConstraint(AllDifferentConstraint())

# Watermelons are the most expensive (rank 5)
problem.addConstraint(lambda watermelons: watermelons == 5, ["watermelons"])

# Peaches are more expensive than loquats (peaches rank < loquats rank)
problem.addConstraint(lambda peaches, loquats: peaches < loquats, ["peaches", "loquats"])

# Plums are the second-cheapest (rank 2)
problem.addConstraint(lambda plums: plums == 2, ["plums"])

# Pears are the third-most expensive (rank 3)
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