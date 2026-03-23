from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (ranks 1 to 7, where 1=cheapest, 7=most expensive)
fruits = ["kiwis", "loquats", "pears", "peaches", "mangoes", "plums", "apples"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "The loquats are the fourth-most expensive" → rank 4
problem.addConstraint(lambda loquats: loquats == 4, ["loquats"])

# "The peaches are less expensive than the mangoes" → peaches < mangoes
problem.addConstraint(lambda peaches, mangoes: peaches < mangoes, ["peaches", "mangoes"])

# "The apples are more expensive than the pears" → apples < pears
problem.addConstraint(lambda apples, pears: apples < pears, ["apples", "pears"])

# "The peaches are the second-most expensive" → rank 6 (since 7=most expensive, 6=second-most)
problem.addConstraint(lambda peaches: peaches == 6, ["peaches"])

# "The plums are the cheapest" → rank 1
problem.addConstraint(lambda plums: plums == 1, ["plums"])

# "The pears are more expensive than the kiwis" → pears < kiwis
problem.addConstraint(lambda pears, kiwis: pears < kiwis, ["pears", "kiwis"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to fruit names
choices = {
    "A": "kiwis",
    "B": "loquats",
    "C": "pears",
    "D": "peaches",
    "E": "mangoes",
    "F": "plums",
    "G": "apples"
}

# Find which fruit has rank 1 (cheapest) and print the corresponding letter
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 1:
            print(letter)