from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (ranks 1 to 7, where 1=cheapest, 7=most expensive)
fruits = ["oranges", "loquats", "apples", "kiwis", "mangoes", "plums", "peaches"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem statements
# "The apples are the second-cheapest" → apples == 2
problem.addConstraint(lambda apples: apples == 2, ["apples"])

# "The peaches are the cheapest" → peaches == 1
problem.addConstraint(lambda peaches: peaches == 1, ["peaches"])

# "The plums are the fourth-most expensive" → rank = 7 - 4 + 1 = 4
problem.addConstraint(lambda plums: plums == 4, ["plums"])

# "The loquats are the third-cheapest" → loquats == 3
problem.addConstraint(lambda loquats: loquats == 3, ["loquats"])

# "The kiwis are more expensive than the mangoes" → mangoes < kiwis
problem.addConstraint(lambda mangoes, kiwis: mangoes < kiwis, ["mangoes", "kiwis"])

# "The oranges are less expensive than the mangoes" → oranges < mangoes
problem.addConstraint(lambda oranges, mangoes: oranges < mangoes, ["oranges", "mangoes"])

# Solve the problem
solutions = problem.getSolutions()

# Determine third-most-expensive fruit (rank = 7 - 3 + 1 = 5)
third_most_expensive_rank = 5

# Map choice letters to fruit names
choices = {
    "A": "oranges",
    "B": "loquats",
    "C": "apples",
    "D": "kiwis",
    "E": "mangoes",
    "F": "plums",
    "G": "peaches"
}

# Find which fruit is at rank 5 and output the corresponding choice letter
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == third_most_expensive_rank:
            print(letter)