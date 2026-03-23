from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=cheapest, 7=most expensive)
fruits = ["oranges", "loquats", "apples", "kiwis", "mangoes", "plums", "peaches"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem statements:
# "The apples are the second-cheapest" → apples == 2
problem.addConstraint(lambda apples: apples == 2, ["apples"])

# "The peaches are the cheapest" → peaches == 1
problem.addConstraint(lambda peaches: peaches == 1, ["peaches"])

# "The plums are the fourth-most expensive" → rank = 4 (since 1=cheapest, 7=most expensive)
# 4th-most-expensive = rank 4 (positions: 7=1st-most-exp, 6=2nd-most-exp, 5=3rd-most-exp, 4=4th-most-exp)
problem.addConstraint(lambda plums: plums == 4, ["plums"])

# "The loquats are the third-cheapest" → loquats == 3
problem.addConstraint(lambda loquats: loquats == 3, ["loquats"])

# "The kiwis are more expensive than the mangoes" → mangoes < kiwis (lower rank = cheaper)
problem.addConstraint(lambda mangoes, kiwis: mangoes < kiwis, ["mangoes", "kiwis"])

# "The oranges are less expensive than the mangoes" → oranges < mangoes
problem.addConstraint(lambda oranges, mangoes: oranges < mangoes, ["oranges", "mangoes"])

# Solve the problem
solutions = problem.getSolutions()

# Find which fruit is third-most-expensive (rank 5)
# Choices mapping:
choices = {
    "A": "oranges",
    "B": "loquats",
    "C": "apples",
    "D": "kiwis",
    "E": "mangoes",
    "F": "plums",
    "G": "peaches"
}

# Since third-most-expensive corresponds to rank 5 (1=cheapest, 7=most expensive)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 5:
            print(letter)