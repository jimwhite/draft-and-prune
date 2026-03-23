from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=least expensive, 5=most expensive)
fruits = ["loquats", "pears", "watermelons", "kiwis", "plums"]
ranks = range(1, 6)
problem.addVariables(fruits, ranks)

# Add constraints
# All fruits have different price ranks
problem.addConstraint(AllDifferentConstraint())

# Loquats are the third-most expensive (rank 3 in our system where higher = more expensive)
problem.addConstraint(lambda loquats: loquats == 3, ["loquats"])

# Loquats are more expensive than watermelons (loquats rank > watermelons rank)
problem.addConstraint(lambda loquats, watermelons: loquats > watermelons, ["loquats", "watermelons"])

# Plums are less expensive than watermelons (plums rank < watermelons rank)
problem.addConstraint(lambda plums, watermelons: plums < watermelons, ["plums", "watermelons"])

# Kiwis are more expensive than pears (kiwis rank > pears rank)
problem.addConstraint(lambda kiwis, pears: kiwis > pears, ["kiwis", "pears"])

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

# Find which fruit has rank 4 (second-most expensive)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 4:
            print(letter)