from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=cheapest, 5=most expensive)
fruits = ["peaches", "mangoes", "kiwis", "oranges", "pears"]
ranks = range(1, 6)
problem.addVariables(fruits, ranks)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on price relationships:
# "The peaches are more expensive than the mangoes" → peaches.rank > mangoes.rank
problem.addConstraint(lambda peaches, mangoes: peaches > mangoes, ("peaches", "mangoes"))

# "The oranges are more expensive than the kiwis" → oranges.rank > kiwis.rank
problem.addConstraint(lambda oranges, kiwis: oranges > kiwis, ("oranges", "kiwis"))

# "The pears are the most expensive" → pears.rank = 5
problem.addConstraint(lambda pears: pears == 5, ("pears",))

# "The mangoes are more expensive than the oranges" → mangoes.rank > oranges.rank
problem.addConstraint(lambda mangoes, oranges: mangoes > oranges, ("mangoes", "oranges"))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to fruit names
choices = {
    "A": "pears",
    "B": "mangoes",
    "C": "kiwis",
    "D": "oranges",
    "E": "peaches"
}

# Find which fruit has rank 2 (second-cheapest)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 2:
            print(letter)