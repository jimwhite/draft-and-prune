from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=cheapest, 7=most expensive)
fruits = ["oranges", "plums", "loquats", "apples", "kiwis", "cantaloupes", "peaches"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add AllDifferent constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem statements
# "The plums are the cheapest" → plums == 1
problem.addConstraint(lambda plums: plums == 1, ["plums"])

# "The apples are the second-cheapest" → apples == 2
problem.addConstraint(lambda apples: apples == 2, ["apples"])

# "The loquats are the fourth-most expensive" → rank 4 (since 1=cheapest, 7=most expensive)
problem.addConstraint(lambda loquats: loquats == 4, ["loquats"])

# "The loquats are less expensive than the kiwis" → loquats < kiwis
problem.addConstraint(lambda loquats, kiwis: loquats < kiwis, ["loquats", "kiwis"])

# "The peaches are more expensive than the kiwis" → kiwis < peaches
problem.addConstraint(lambda kiwis, peaches: kiwis < peaches, ["kiwis", "peaches"])

# "The peaches are less expensive than the oranges" → peaches < oranges
problem.addConstraint(lambda peaches, oranges: peaches < oranges, ["peaches", "oranges"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to fruit names
choices = {
    "A": "oranges",
    "B": "plums",
    "C": "loquats",
    "D": "apples",
    "E": "kiwis",
    "F": "cantaloupes",
    "G": "peaches"
}

# Find which fruit is second-most expensive (rank 6)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 6:
            print(letter)