from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
fruits = ["mangoes", "kiwis", "watermelons", "oranges", "apples"]
ranks = range(1, 6)  # 1=cheapest, 5=most expensive
problem.addVariables(fruits, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The oranges are the cheapest."
problem.addConstraint(lambda oranges: oranges == 1, ["oranges"])

# "The kiwis are less expensive than the mangoes."
problem.addConstraint(lambda kiwis, mangoes: kiwis < mangoes, ["kiwis", "mangoes"])

# "The watermelons are more expensive than the apples."
problem.addConstraint(lambda apples, watermelons: apples < watermelons, ["apples", "watermelons"])

# "The watermelons are less expensive than the kiwis."
problem.addConstraint(lambda watermelons, kiwis: watermelons < kiwis, ["watermelons", "kiwis"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to fruit names
choices = {
    "A": "mangoes",
    "B": "kiwis",
    "C": "watermelons",
    "D": "oranges",
    "E": "apples"
}

# Find the fruit with rank 2 (second-cheapest)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 2:
            print(letter)