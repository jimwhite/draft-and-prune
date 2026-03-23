from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=cheapest, 3=most expensive)
fruits = ["mangoes", "watermelons", "kiwis"]
ranks = range(1, 4)
problem.addVariables(fruits, ranks)

# Add constraints based on the problem description
# 1. All fruits must have different price ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The watermelons are less expensive than the kiwis" -> watermelons < kiwis
problem.addConstraint(lambda watermelons, kiwis: watermelons < kiwis, ("watermelons", "kiwis"))

# 3. "The kiwis are the second-most expensive" -> kiwis == 2 (since 1=cheapest, 2=middle, 3=most expensive)
problem.addConstraint(lambda kiwis: kiwis == 2, ("kiwis",))

# Solve for the arrangement
solutions = problem.getSolutions()

# Map choice letters to fruit names
choices = {
    "A": "mangoes",
    "B": "watermelons",
    "C": "kiwis"
}

# Find which fruit has rank 1 (cheapest) and print the corresponding letter
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 1:
            print(letter)