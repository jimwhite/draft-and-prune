from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (price ranks 1-7, where 1=cheapest)
fruits = ["mangoes", "watermelons", "peaches", "kiwis", "oranges", "cantaloupes", "plums"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem statements:
# 1. "The watermelons are the cheapest." → watermelons == 1
problem.addConstraint(lambda watermelons: watermelons == 1, ["watermelons"])

# 2. "The peaches are more expensive than the mangoes." → mangoes < peaches
problem.addConstraint(lambda mangoes, peaches: mangoes < peaches, ["mangoes", "peaches"])

# 3. "The cantaloupes are the second-most expensive." → cantaloupes == 6
problem.addConstraint(lambda cantaloupes: cantaloupes == 6, ["cantaloupes"])

# 4. "The oranges are more expensive than the cantaloupes." → cantaloupes < oranges
problem.addConstraint(lambda cantaloupes, oranges: cantaloupes < oranges, ["cantaloupes", "oranges"])

# 5. "The peaches are less expensive than the plums." → peaches < plums
problem.addConstraint(lambda peaches, plums: peaches < plums, ["peaches", "plums"])

# 6. "The kiwis are the third-cheapest." → kiwis == 3
problem.addConstraint(lambda kiwis: kiwis == 3, ["kiwis"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to fruit names
choices = {
    "A": "mangoes",
    "B": "watermelons",
    "C": "peaches",
    "D": "kiwis",
    "E": "oranges",
    "F": "cantaloupes",
    "G": "plums"
}

# Find which fruit has rank 1 (cheapest) and print the corresponding letter
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 1:
            print(letter)