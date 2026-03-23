from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (the seven fruits) and domain (price ranks 1 to 7, where 1=cheapest, 7=most expensive)
fruits = ["plums", "kiwis", "pears", "mangoes", "apples", "oranges", "loquats"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add constraints based on the problem description
# 1. All fruits have different price ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The pears are less expensive than the oranges" → pears < oranges
problem.addConstraint(lambda pears, oranges: pears < oranges, ("pears", "oranges"))

# 3. "The mangoes are less expensive than the kiwis" → mangoes < kiwis
problem.addConstraint(lambda mangoes, kiwis: mangoes < kiwis, ("mangoes", "kiwis"))

# 4. "The plums are the second-most expensive" → plums == 6 (since 7 is most expensive)
problem.addConstraint(lambda plums: plums == 6, ("plums",))

# 5. "The loquats are more expensive than the apples" → loquats > apples
problem.addConstraint(lambda loquats, apples: loquats > apples, ("loquats", "apples"))

# 6. "The kiwis are less expensive than the apples" → kiwis < apples
problem.addConstraint(lambda kiwis, apples: kiwis < apples, ("kiwis", "apples"))

# 7. "The loquats are the fourth-most expensive" → loquats == 4
problem.addConstraint(lambda loquats: loquats == 4, ("loquats",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to fruit names
choices = {
    'A': 'plums',
    'B': 'kiwis',
    'C': 'pears',
    'D': 'mangoes',
    'E': 'apples',
    'F': 'oranges',
    'G': 'loquats'
}

# Find which fruit has rank 3 (third-cheapest)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 3:
            print(letter)