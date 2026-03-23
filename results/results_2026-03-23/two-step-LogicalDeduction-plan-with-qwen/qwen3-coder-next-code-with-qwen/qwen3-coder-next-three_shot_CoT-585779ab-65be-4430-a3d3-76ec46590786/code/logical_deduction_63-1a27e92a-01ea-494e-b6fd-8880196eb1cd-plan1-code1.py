from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=cheapest, 5=most expensive)
fruits = ["cantaloupes", "kiwis", "oranges", "mangoes", "peaches"]
ranks = range(1, 6)
problem.addVariables(fruits, ranks)

# Add constraints based on the problem description
# 1. All fruits have different price ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The kiwis are less expensive than the mangoes" → kiwis < mangoes
problem.addConstraint(lambda kiwis, mangoes: kiwis < mangoes, ("kiwis", "mangoes"))

# 3. "The peaches are less expensive than the oranges" → peaches < oranges
problem.addConstraint(lambda peaches, oranges: peaches < oranges, ("peaches", "oranges"))

# 4. "The oranges are the second-most expensive" → rank = 4 (since 5 is most expensive)
problem.addConstraint(lambda oranges: oranges == 4, ("oranges",))

# 5. "The mangoes are the second-cheapest" → rank = 2 (since 1 is cheapest)
problem.addConstraint(lambda mangoes: mangoes == 2, ("mangoes",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to fruit names
choices = {
    "A": "cantaloupes",
    "B": "kiwis",
    "C": "oranges",
    "D": "mangoes",
    "E": "peaches"
}

# Find the fruit with rank 1 (cheapest) and print corresponding choice letter
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 1:
            print(letter)