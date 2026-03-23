from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (ranks 1 to 7, where 1=cheapest, 7=most expensive)
fruits = ["oranges", "plums", "loquats", "apples", "kiwis", "cantaloupes", "peaches"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add AllDifferent constraint
problem.addConstraint(AllDifferentConstraint())

# Add fixed value constraints based on statements
# "The plums are the cheapest" → plums = 1
problem.addConstraint(lambda p: p == 1, ["plums"])

# "The apples are the second-cheapest" → apples = 2
problem.addConstraint(lambda a: a == 2, ["apples"])

# "The loquats are the fourth-most expensive" → rank = 4 (since most expensive=7, 4th-most expensive is rank 4)
problem.addConstraint(lambda l: l == 4, ["loquats"])

# Add inequality constraints
# "The loquats are less expensive than the kiwis" → loquats < kiwis
problem.addConstraint(lambda l, k: l < k, ["loquats", "kiwis"])

# "The peaches are more expensive than the kiwis" → kiwis < peaches
problem.addConstraint(lambda k, p: k < p, ["kiwis", "peaches"])

# "The peaches are less expensive than the oranges" → peaches < oranges
problem.addConstraint(lambda p, o: p < o, ["peaches", "oranges"])

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

# Find the fruit with rank 6 (second-most expensive)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 6:
            print(letter)