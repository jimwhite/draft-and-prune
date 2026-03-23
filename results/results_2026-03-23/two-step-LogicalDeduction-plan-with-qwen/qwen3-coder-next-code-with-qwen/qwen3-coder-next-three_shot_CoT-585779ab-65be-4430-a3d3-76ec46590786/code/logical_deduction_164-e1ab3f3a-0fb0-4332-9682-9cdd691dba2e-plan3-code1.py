from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
fruits = ["mangoes", "kiwis", "oranges", "watermelons", "apples", "pears", "loquats"]
ranks = range(1, 8)  # 1=cheapest, 7=most expensive
problem.addVariables(fruits, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The loquats are less expensive than the oranges" → loquats < oranges
problem.addConstraint(lambda loquats, oranges: loquats < oranges, ("loquats", "oranges"))

# "The oranges are the third-most expensive" → oranges == 5 (since 7-2=5)
problem.addConstraint(lambda oranges: oranges == 5, ("oranges",))

# "The apples are the cheapest" → apples == 1
problem.addConstraint(lambda apples: apples == 1, ("apples",))

# "The kiwis are more expensive than the pears" → kiwis > pears
problem.addConstraint(lambda kiwis, pears: kiwis > pears, ("kiwis", "pears"))

# "The mangoes are more expensive than the watermelons" → mangoes > watermelons
problem.addConstraint(lambda mangoes, watermelons: mangoes > watermelons, ("mangoes", "watermelons"))

# "The loquats are more expensive than the kiwis" → loquats > kiwis
problem.addConstraint(lambda loquats, kiwis: loquats > kiwis, ("loquats", "kiwis"))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to fruit names
choices = {
    'A': "mangoes",
    'B': "kiwis",
    'C': "oranges",
    'D': "watermelons",
    'E': "apples",
    'F': "pears",
    'G': "loquats"
}

# Find the fruit with rank 7 (most expensive)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 7:
            print(letter)