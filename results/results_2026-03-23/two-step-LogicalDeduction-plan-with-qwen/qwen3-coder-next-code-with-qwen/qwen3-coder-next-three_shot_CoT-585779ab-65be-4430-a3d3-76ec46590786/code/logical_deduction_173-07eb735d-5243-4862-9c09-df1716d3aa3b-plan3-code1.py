from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (ranks 1 to 7, where 1=cheapest, 7=most expensive)
fruits = ["loquats", "peaches", "watermelons", "plums", "kiwis", "mangoes", "pears"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem description:
# 1. "The pears are more expensive than the kiwis" → pears > kiwis
problem.addConstraint(lambda k, p: p > k, ("kiwis", "pears"))

# 2. "The watermelons are less expensive than the peaches" → watermelons < peaches
problem.addConstraint(lambda w, pe: w < pe, ("watermelons", "peaches"))

# 3. "The mangoes are the third-cheapest" → mangoes == 3
problem.addConstraint(lambda m: m == 3, ("mangoes",))

# 4. "The watermelons are the third-most expensive" → third-most expensive = 7 - 2 = 5
problem.addConstraint(lambda w: w == 5, ("watermelons",))

# 5. "The plums are the second-most expensive" → second-most expensive = 7 - 1 = 6
problem.addConstraint(lambda p: p == 6, ("plums",))

# 6. "The loquats are the second-cheapest" → loquats == 2
problem.addConstraint(lambda l: l == 2, ("loquats",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to fruit names
choices = {
    "A": "loquats",
    "B": "peaches",
    "C": "watermelons",
    "D": "plums",
    "E": "kiwis",
    "F": "mangoes",
    "G": "pears"
}

# Find which fruit has rank 6 (second-most expensive)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 6:
            print(letter)