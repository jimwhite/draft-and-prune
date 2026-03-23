from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (price ranks 1 to 7, where 1=cheapest, 7=most expensive)
fruits = ["oranges", "loquats", "apples", "kiwis", "mangoes", "plums", "peaches"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add AllDifferentConstraint to ensure each fruit has a unique rank
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on explicit rank statements:
# "The apples are the second-cheapest" → apples == 2
problem.addConstraint(lambda apples: apples == 2, ["apples"])

# "The peaches are the cheapest" → peaches == 1
problem.addConstraint(lambda peaches: peaches == 1, ["peaches"])

# "The plums are the fourth-most expensive" → plums == 4
problem.addConstraint(lambda plums: plums == 4, ["plums"])

# "The loquats are the third-cheapest" → loquats == 3
problem.addConstraint(lambda loquats: loquats == 3, ["loquats"])

# Add constraints based on relative ordering:
# "The kiwis are more expensive than the mangoes" → kiwis > mangoes
problem.addConstraint(lambda kiwis, mangoes: kiwis > mangoes, ["kiwis", "mangoes"])

# "The oranges are less expensive than the mangoes" → oranges < mangoes
problem.addConstraint(lambda oranges, mangoes: oranges < mangoes, ["oranges", "mangoes"])

# Solve the problem
solutions = problem.getSolutions()

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

# Find which fruit has rank 7 (most expensive) and print the corresponding letter
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 7:
            print(letter)