from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (ranks 1 to 7, where 1=cheapest, 7=most expensive)
fruits = ["mangoes", "kiwis", "oranges", "watermelons", "apples", "pears", "loquats"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem description:
# 1. "The apples are the cheapest." → rank 1
problem.addConstraint(lambda apples: apples == 1, ["apples"])

# 2. "The oranges are the third-most expensive." → rank 3
problem.addConstraint(lambda oranges: oranges == 3, ["oranges"])

# 3. "The loquats are less expensive than the oranges." → loquats < oranges (loquats < 3)
problem.addConstraint(lambda loquats, oranges: loquats < oranges, ["loquats", "oranges"])

# 4. "The kiwis are more expensive than the pears." → kiwis > pears
problem.addConstraint(lambda kiwis, pears: kiwis > pears, ["kiwis", "pears"])

# 5. "The mangoes are more expensive than the watermelons." → mangoes > watermelons
problem.addConstraint(lambda mangoes, watermelons: mangoes > watermelons, ["mangoes", "watermelons"])

# 6. "The loquats are more expensive than the kiwis." → loquats > kiwis
problem.addConstraint(lambda loquats, kiwis: loquats > kiwis, ["loquats", "kiwis"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to fruit names
choices = {
    "A": "mangoes",
    "B": "kiwis",
    "C": "oranges",
    "D": "watermelons",
    "E": "apples",
    "F": "pears",
    "G": "loquats"
}

# Find the fruit with rank 4 (fourth-most expensive)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 4:
            print(letter)