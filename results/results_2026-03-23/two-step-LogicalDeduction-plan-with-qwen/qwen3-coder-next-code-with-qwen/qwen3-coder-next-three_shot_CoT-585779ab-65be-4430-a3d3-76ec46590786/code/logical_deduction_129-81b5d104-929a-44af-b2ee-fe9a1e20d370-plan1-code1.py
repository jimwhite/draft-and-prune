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
# 1. "The loquats are the fourth-most expensive" → loquats == 4
problem.addConstraint(lambda loquats: loquats == 4, ["loquats"])

# 2. "The peaches are less expensive than the mangoes" → peaches < mangoes
problem.addConstraint(lambda peaches, mangoes: peaches < mangoes, ["peaches", "mangoes"])

# 3. "The apples are more expensive than the pears" → apples < pears
problem.addConstraint(lambda apples, pears: apples < pears, ["apples", "pears"])

# 4. "The peaches are the second-most expensive" → peaches == 2
problem.addConstraint(lambda peaches: peaches == 2, ["peaches"])

# 5. "The plums are the cheapest" → plums == 1
problem.addConstraint(lambda plums: plums == 1, ["plums"])

# 6. "The pears are more expensive than the kiwis" → pears < kiwis
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

# Find which fruit has rank 1 (cheapest) and print the corresponding choice letter
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 1:
            print(letter)