from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define the seven fruits as variables
fruits = ["kiwis", "cantaloupes", "oranges", "loquats", "pears", "watermelons", "peaches"]

# Define the domain: integers 1 to 7, where 1 = cheapest, 7 = most expensive
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add constraints based on the problem description
# 1. All fruits have different price ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The loquats are less expensive than the peaches" → loquats < peaches
problem.addConstraint(lambda loquats, peaches: loquats < peaches, ("loquats", "peaches"))

# 3. "The pears are the third-cheapest" → pears == 3
problem.addConstraint(lambda pears: pears == 3, ("pears",))

# 4. "The oranges are less expensive than the cantaloupes" → oranges < cantaloupes
problem.addConstraint(lambda oranges, cantaloupes: oranges < cantaloupes, ("oranges", "cantaloupes"))

# 5. "The loquats are more expensive than the watermelons" → watermelons < loquats
problem.addConstraint(lambda watermelons, loquats: watermelons < loquats, ("watermelons", "loquats"))

# 6. "The peaches are less expensive than the oranges" → peaches < oranges
problem.addConstraint(lambda peaches, oranges: peaches < oranges, ("peaches", "oranges"))

# 7. "The kiwis are the second-most expensive" → kiwis == 6
problem.addConstraint(lambda kiwis: kiwis == 6, ("kiwis",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to fruit names in order: A=kiwis, B=cantaloupes, C=oranges, D=loquats, E=pears, F=watermelons, G=peaches
choices = {
    "A": "kiwis",
    "B": "cantaloupes",
    "C": "oranges",
    "D": "loquats",
    "E": "pears",
    "F": "watermelons",
    "G": "peaches"
}

# Find which fruit has rank 2 (second-cheapest)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 2:
            print(letter)