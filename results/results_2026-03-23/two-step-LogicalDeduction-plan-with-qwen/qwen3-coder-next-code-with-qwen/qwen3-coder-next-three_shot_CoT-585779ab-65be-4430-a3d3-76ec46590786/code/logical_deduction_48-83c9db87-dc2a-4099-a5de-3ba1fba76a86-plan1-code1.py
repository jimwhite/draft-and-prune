from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=cheapest, 5=most expensive)
fruits = ["mangoes", "kiwis", "watermelons", "oranges", "apples"]
ranks = range(1, 6)
problem.addVariables(fruits, ranks)

# Add constraints based on the problem description
# 1. All fruits have different price ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The oranges are the cheapest."
problem.addConstraint(lambda oranges: oranges == 1, ["oranges"])

# 3. "The kiwis are less expensive than the mangoes."
problem.addConstraint(lambda kiwis, mangoes: kiwis < mangoes, ["kiwis", "mangoes"])

# 4. "The watermelons are more expensive than the apples."
problem.addConstraint(lambda apples, watermelons: apples < watermelons, ["apples", "watermelons"])

# 5. "The watermelons are less expensive than the kiwis."
problem.addConstraint(lambda watermelons, kiwis: watermelons < kiwis, ["watermelons", "kiwis"])

# Solve for all valid arrangements
solutions = problem.getSolutions()

# Map choice letters to fruit names
choices = {
    "A": "mangoes",
    "B": "kiwis",
    "C": "watermelons",
    "D": "oranges",
    "E": "apples"
}

# Find the fruit with rank 5 (most expensive) and print corresponding choice letter
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 5:
            print(letter)