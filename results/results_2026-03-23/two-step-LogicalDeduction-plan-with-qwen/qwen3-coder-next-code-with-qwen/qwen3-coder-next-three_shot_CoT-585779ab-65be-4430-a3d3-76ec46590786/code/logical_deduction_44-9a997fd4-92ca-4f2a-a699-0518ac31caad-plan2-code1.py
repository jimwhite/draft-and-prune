from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=cheapest, 5=most expensive)
fruits = ["pears", "mangoes", "kiwis", "oranges", "peaches"]
ranks = range(1, 6)
problem.addVariables(fruits, ranks)

# Add constraints based on the problem description
# 1. All fruits have different price ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The peaches are more expensive than the mangoes" → peaches > mangoes
problem.addConstraint(lambda peaches, mangoes: peaches > mangoes, ("peaches", "mangoes"))

# 3. "The oranges are more expensive than the kiwis" → oranges > kiwis
problem.addConstraint(lambda oranges, kiwis: oranges > kiwis, ("oranges", "kiwis"))

# 4. "The pears are the most expensive" → pears == 5
problem.addConstraint(lambda pears: pears == 5, ("pears",))

# 5. "The mangoes are more expensive than the oranges" → mangoes > oranges
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