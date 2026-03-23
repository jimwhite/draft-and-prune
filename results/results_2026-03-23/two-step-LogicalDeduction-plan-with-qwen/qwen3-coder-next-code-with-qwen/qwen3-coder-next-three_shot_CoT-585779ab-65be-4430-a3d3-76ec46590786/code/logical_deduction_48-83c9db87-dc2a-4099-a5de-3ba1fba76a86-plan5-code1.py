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

# Oranges are the cheapest (rank 1)
problem.addConstraint(lambda oranges: oranges == 1, ["oranges"])

# Kiwis are less expensive than mangoes (kiwis rank < mangoes rank)
problem.addConstraint(lambda kiwis, mangoes: kiwis < mangoes, ["kiwis", "mangoes"])

# Watermelons are more expensive than apples (apples rank < watermelons rank)
problem.addConstraint(lambda apples, watermelons: apples < watermelons, ["apples", "watermelons"])

# Watermelons are less expensive than kiwis (watermelons rank < kiwis rank)
problem.addConstraint(lambda watermelons, kiwis: watermelons < kiwis, ["watermelons", "kiwis"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to fruit names
choices = {
    "A": "mangoes",
    "B": "kiwis",
    "C": "watermelons",
    "D": "oranges",
    "E": "apples"
}

# Find the most expensive fruit (rank 5) and print corresponding choice letter
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 5:
            print(letter)