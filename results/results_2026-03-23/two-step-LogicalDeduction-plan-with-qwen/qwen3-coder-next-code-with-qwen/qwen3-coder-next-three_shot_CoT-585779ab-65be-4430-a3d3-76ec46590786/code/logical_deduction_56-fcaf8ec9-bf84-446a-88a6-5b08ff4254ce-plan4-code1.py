from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=cheapest, 5=most expensive)
fruits = ["mangoes", "kiwis", "watermelons", "oranges", "apples"]
ranks = range(1, 6)
problem.addVariables(fruits, ranks)

# Add constraints
# All fruits have different price ranks
problem.addConstraint(AllDifferentConstraint())

# The oranges are the cheapest (rank 1)
problem.addConstraint(lambda oranges: oranges == 1, ["oranges"])

# The kiwis are less expensive than the mangoes (kiwis < mangoes)
problem.addConstraint(lambda kiwis, mangoes: kiwis < mangoes, ["kiwis", "mangoes"])

# The watermelons are more expensive than the apples (apples < watermelons)
problem.addConstraint(lambda apples, watermelons: apples < watermelons, ["apples", "watermelons"])

# The watermelons are less expensive than the kiwis (watermelons < kiwis)
problem.addConstraint(lambda watermelons, kiwis: watermelons < kiwis, ["watermelons", "kiwis"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to fruit names for the second-cheapest position (rank 2)
choices = {
    "A": "mangoes",
    "B": "kiwis",
    "C": "watermelons",
    "D": "oranges",
    "E": "apples"
}

# Find which fruit has rank 2 and print the corresponding choice letter
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 2:
            print(letter)