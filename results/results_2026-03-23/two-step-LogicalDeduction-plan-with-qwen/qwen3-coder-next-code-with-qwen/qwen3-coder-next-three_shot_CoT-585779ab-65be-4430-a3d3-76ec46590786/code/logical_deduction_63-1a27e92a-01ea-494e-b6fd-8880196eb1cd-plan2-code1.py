from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=cheapest, 5=most expensive)
fruits = ["cantaloupes", "kiwis", "oranges", "mangoes", "peaches"]
ranks = range(1, 6)
problem.addVariables(fruits, ranks)

# Add constraints
# All fruits have different price ranks
problem.addConstraint(AllDifferentConstraint())

# The kiwis are less expensive than the mangoes → kiwis < mangoes
problem.addConstraint(lambda kiwis, mangoes: kiwis < mangoes, ("kiwis", "mangoes"))

# The peaches are less expensive than the oranges → peaches < oranges
problem.addConstraint(lambda peaches, oranges: peaches < oranges, ("peaches", "oranges"))

# The oranges are the second-most expensive → oranges == 4
problem.addConstraint(lambda oranges: oranges == 4, ("oranges",))

# The mangoes are the second-cheapest → mangoes == 2
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

# Find which fruit is the cheapest (rank 1) and print corresponding letter
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 1:
            print(letter)