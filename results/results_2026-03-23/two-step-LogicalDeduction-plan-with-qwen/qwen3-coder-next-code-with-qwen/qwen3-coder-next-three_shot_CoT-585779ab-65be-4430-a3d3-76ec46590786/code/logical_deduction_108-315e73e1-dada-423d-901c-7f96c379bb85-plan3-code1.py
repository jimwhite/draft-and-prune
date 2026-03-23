from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (the seven fruits)
fruits = ["loquats", "peaches", "watermelons", "plums", "kiwis", "mangoes", "pears"]

# Define domain: 1 = cheapest, 7 = most expensive
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add AllDifferent constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem description:
# 1. "The pears are more expensive than the kiwis" → kiwis < pears
problem.addConstraint(lambda kiwis, pears: kiwis < pears, ("kiwis", "pears"))

# 2. "The watermelons are less expensive than the peaches" → watermelons < peaches
problem.addConstraint(lambda watermelons, peaches: watermelons < peaches, ("watermelons", "peaches"))

# 3. "The mangoes are the third-cheapest" → mangoes == 3
problem.addConstraint(lambda mangoes: mangoes == 3, ("mangoes",))

# 4. "The watermelons are the third-most expensive" → watermelons == 5
problem.addConstraint(lambda watermelons: watermelons == 5, ("watermelons",))

# 5. "The plums are the second-most expensive" → plums == 6
problem.addConstraint(lambda plums: plums == 6, ("plums",))

# 6. "The loquats are the second-cheapest" → loquats == 2
problem.addConstraint(lambda loquats: loquats == 2, ("loquats",))

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

# Find which fruit has rank 5 (third-most expensive)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 5:
            print(letter)