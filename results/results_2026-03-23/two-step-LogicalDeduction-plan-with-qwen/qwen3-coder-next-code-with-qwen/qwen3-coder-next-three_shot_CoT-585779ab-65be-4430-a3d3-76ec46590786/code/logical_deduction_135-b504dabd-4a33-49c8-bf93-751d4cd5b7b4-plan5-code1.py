from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=least expensive, 7=most expensive)
fruits = ["plums", "kiwis", "pears", "mangoes", "apples", "oranges", "loquats"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add AllDifferent constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# "The pears are less expensive than the oranges" → pears < oranges
problem.addConstraint(lambda pears, oranges: pears < oranges, ("pears", "oranges"))

# "The mangoes are less expensive than the kiwis" → mangoes < kiwis
problem.addConstraint(lambda mangoes, kiwis: mangoes < kiwis, ("mangoes", "kiwis"))

# "The plums are the second-most expensive" → plums == 6
problem.addConstraint(lambda plums: plums == 6, ("plums",))

# "The loquats are more expensive than the apples" → loquats > apples
problem.addConstraint(lambda loquats, apples: loquats > apples, ("loquats", "apples"))

# "The kiwis are less expensive than the apples" → kiwis < apples
problem.addConstraint(lambda kiwis, apples: kiwis < apples, ("kiwis", "apples"))

# "The loquats are the fourth-most expensive" → loquats == 4
problem.addConstraint(lambda loquats: loquats == 4, ("loquats",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to fruit names
choices = {
    "A": "plums",
    "B": "kiwis",
    "C": "pears",
    "D": "mangoes",
    "E": "apples",
    "F": "oranges",
    "G": "loquats"
}

# Find which fruit has rank 7 (most expensive)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 7:
            print(letter)