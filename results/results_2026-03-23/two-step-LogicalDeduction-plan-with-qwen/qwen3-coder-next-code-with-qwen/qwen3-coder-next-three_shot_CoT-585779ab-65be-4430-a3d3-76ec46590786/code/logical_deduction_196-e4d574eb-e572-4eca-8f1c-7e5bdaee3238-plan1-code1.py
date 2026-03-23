from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (price ranks 1-7, where 1=cheapest, 7=most expensive)
fruits = ["oranges", "loquats", "apples", "kiwis", "mangoes", "plums", "peaches"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem description
# "The apples are the second-cheapest" → rank 2
problem.addConstraint(lambda apples: apples == 2, ["apples"])

# "The peaches are the cheapest" → rank 1
problem.addConstraint(lambda peaches: peaches == 1, ["peaches"])

# "The plums are the fourth-most expensive" → rank 4 (since 7=1st most expensive, 6=2nd, 5=3rd, 4=4th)
problem.addConstraint(lambda plums: plums == 4, ["plums"])

# "The loquats are the third-cheapest" → rank 3
problem.addConstraint(lambda loquats: loquats == 3, ["loquats"])

# "The kiwis are more expensive than the mangoes" → mangoes < kiwis
problem.addConstraint(lambda mangoes, kiwis: mangoes < kiwis, ["mangoes", "kiwis"])

# "The oranges are less expensive than the mangoes" → oranges < mangoes
problem.addConstraint(lambda oranges, mangoes: oranges < mangoes, ["oranges", "mangoes"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to fruit names
choices = {
    'A': 'oranges',
    'B': 'loquats',
    'C': 'apples',
    'D': 'kiwis',
    'E': 'mangoes',
    'F': 'plums',
    'G': 'peaches'
}

# Find the third-most expensive fruit (rank 5, since 7=1st most expensive, 6=2nd, 5=3rd)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 5:
            print(letter)