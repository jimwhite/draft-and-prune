from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=cheapest, 5=most expensive)
fruits = ["watermelons", "oranges", "loquats", "plums", "kiwis"]
ranks = range(1, 6)
problem.addVariables(fruits, ranks)

# Add constraints based on the statements
# All fruits have different price ranks
problem.addConstraint(AllDifferentConstraint())

# "The plums are less expensive than the kiwis" → plums rank < kiwis rank
problem.addConstraint(lambda plums, kiwis: plums < kiwis, ("plums", "kiwis"))

# "The plums are more expensive than the watermelons" → plums rank > watermelons rank
problem.addConstraint(lambda plums, watermelons: plums > watermelons, ("plums", "watermelons"))

# "The loquats are more expensive than the kiwis" → loquats rank < kiwis rank
problem.addConstraint(lambda loquats, kiwis: loquats < kiwis, ("loquats", "kiwis"))

# "The oranges are the most expensive" → oranges rank = 5
problem.addConstraint(lambda oranges: oranges == 5, ("oranges",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to fruit names
choices = {
    "A": "watermelons",
    "B": "oranges",
    "C": "loquats",
    "D": "plums",
    "E": "kiwis"
}

# Find which fruit has rank 2 (second-cheapest)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 2:
            print(letter)