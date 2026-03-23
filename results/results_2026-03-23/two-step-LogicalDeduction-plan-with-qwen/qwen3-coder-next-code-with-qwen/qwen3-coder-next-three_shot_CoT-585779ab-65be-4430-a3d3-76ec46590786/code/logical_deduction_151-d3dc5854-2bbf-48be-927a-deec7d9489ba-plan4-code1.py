from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=cheapest, 7=most expensive)
fruits = ["watermelons", "mangoes", "kiwis", "pears", "cantaloupes", "oranges", "peaches"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add AllDifferentConstraint to ensure all prices are distinct
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem statements:
# "The oranges are more expensive than the peaches" → oranges > peaches
problem.addConstraint(lambda oranges, peaches: oranges > peaches, ("oranges", "peaches"))

# "The cantaloupes are the fourth-most expensive" → rank 4 (since 7=most, 6=2nd-most, 5=3rd-most, 4=4th-most)
problem.addConstraint(lambda cantaloupes: cantaloupes == 4, ("cantaloupes",))

# "The pears are less expensive than the cantaloupes" → pears < cantaloupes
problem.addConstraint(lambda pears, cantaloupes: pears < cantaloupes, ("pears", "cantaloupes"))

# "The peaches are the second-most expensive" → rank 6 (since most=7, second-most=6)
problem.addConstraint(lambda peaches: peaches == 6, ("peaches",))

# "The mangoes are the cheapest" → rank 1
problem.addConstraint(lambda mangoes: mangoes == 1, ("mangoes",))

# "The kiwis are the third-cheapest" → rank 3 (1=cheapest, 2=second-cheapest, 3=third-cheapest)
problem.addConstraint(lambda kiwis: kiwis == 3, ("kiwis",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to fruit names
choices = {
    'A': "watermelons",
    'B': "mangoes",
    'C': "kiwis",
    'D': "pears",
    'E': "cantaloupes",
    'F': "oranges",
    'G': "peaches"
}

# Find which fruit has rank 6 (second-most expensive) and print the corresponding letter
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 6:
            print(letter)