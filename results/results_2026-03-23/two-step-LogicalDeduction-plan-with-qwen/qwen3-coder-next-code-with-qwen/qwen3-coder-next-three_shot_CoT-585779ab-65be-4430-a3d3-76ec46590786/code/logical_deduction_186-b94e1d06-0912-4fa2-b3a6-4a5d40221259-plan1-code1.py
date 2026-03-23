from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (price ranks 1 to 7, where 1=cheapest, 7=most expensive)
fruits = ["kiwis", "plums", "mangoes", "watermelons", "pears", "peaches", "oranges"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add all different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem statements:
# "The pears are the third-cheapest" → pears == 3
problem.addConstraint(lambda pears: pears == 3, ["pears"])

# "The kiwis are the second-most expensive" → kiwis == 6 (since 7 is most expensive)
problem.addConstraint(lambda kiwis: kiwis == 6, ["kiwis"])

# "The pears are more expensive than the plums" → plums < pears
problem.addConstraint(lambda plums, pears: plums < pears, ["plums", "pears"])

# "The oranges are less expensive than the kiwis" → oranges < kiwis
problem.addConstraint(lambda oranges, kiwis: oranges < kiwis, ["oranges", "kiwis"])

# "The mangoes are the third-most expensive" → mangoes == 5 (7-3+1=5)
problem.addConstraint(lambda mangoes: mangoes == 5, ["mangoes"])

# "The peaches are the second-cheapest" → peaches == 2
problem.addConstraint(lambda peaches: peaches == 2, ["peaches"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to fruits
choices = {
    "A": "kiwis",
    "B": "plums",
    "C": "mangoes",
    "D": "watermelons",
    "E": "pears",
    "F": "peaches",
    "G": "oranges"
}

# Find the cheapest fruit (rank 1) and print corresponding choice letter
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 1:
            print(letter)