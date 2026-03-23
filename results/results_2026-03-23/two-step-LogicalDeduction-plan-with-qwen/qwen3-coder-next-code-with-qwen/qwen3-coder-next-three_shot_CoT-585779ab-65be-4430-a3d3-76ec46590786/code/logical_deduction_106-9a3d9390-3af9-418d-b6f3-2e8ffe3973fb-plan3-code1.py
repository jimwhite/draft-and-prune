from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=cheapest, 7=most expensive)
fruits = ["watermelons", "cantaloupes", "pears", "peaches", "mangoes", "kiwis", "oranges"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Translate statements into constraints:
# "The oranges are more expensive than the cantaloupes" → cantaloupes < oranges
problem.addConstraint(lambda cantaloupes, oranges: cantaloupes < oranges, ("cantaloupes", "oranges"))

# "The pears are less expensive than the kiwis" → pears < kiwis
problem.addConstraint(lambda pears, kiwis: pears < kiwis, ("pears", "kiwis"))

# "The kiwis are the fourth-most expensive" → kiwis == 4
problem.addConstraint(lambda kiwis: kiwis == 4, ("kiwis",))

# "The mangoes are less expensive than the pears" → mangoes < pears
problem.addConstraint(lambda mangoes, pears: mangoes < pears, ("mangoes", "pears"))

# "The peaches are the cheapest" → peaches == 1
problem.addConstraint(lambda peaches: peaches == 1, ("peaches",))

# "The cantaloupes are more expensive than the watermelons" → watermelons < cantaloupes
problem.addConstraint(lambda watermelons, cantaloupes: watermelons < cantaloupes, ("watermelons", "cantaloupes"))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to fruit names
choices = {
    "A": "watermelons",
    "B": "cantaloupes",
    "C": "pears",
    "D": "peaches",
    "E": "mangoes",
    "F": "kiwis",
    "G": "oranges"
}

# Find which fruit has rank 4 (fourth-most expensive)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 4:
            print(letter)