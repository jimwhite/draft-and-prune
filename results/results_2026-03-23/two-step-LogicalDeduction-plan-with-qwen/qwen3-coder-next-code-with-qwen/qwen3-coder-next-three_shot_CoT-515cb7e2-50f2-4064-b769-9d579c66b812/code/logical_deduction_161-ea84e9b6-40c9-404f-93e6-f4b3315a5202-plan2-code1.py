from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=cheapest, 7=most expensive)
fruits = ["kiwis", "cantaloupes", "oranges", "loquats", "pears", "watermelons", "peaches"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "The loquats are less expensive than the peaches" → loquats < peaches
problem.addConstraint(lambda loquats, peaches: loquats < peaches, ("loquats", "peaches"))

# "The pears are the third-cheapest" → pears == 3
problem.addConstraint(lambda pears: pears == 3, ("pears",))

# "The oranges are less expensive than the cantaloupes" → oranges < cantaloupes
problem.addConstraint(lambda oranges, cantaloupes: oranges < cantaloupes, ("oranges", "cantaloupes"))

# "The loquats are more expensive than the watermelons" → watermelons < loquats
problem.addConstraint(lambda watermelons, loquats: watermelons < loquats, ("watermelons", "loquats"))

# "The peaches are less expensive than the oranges" → peaches < oranges
problem.addConstraint(lambda peaches, oranges: peaches < oranges, ("peaches", "oranges"))

# "The kiwis are the second-most expensive" → kiwis == 6 (since 7 is most expensive)
problem.addConstraint(lambda kiwis: kiwis == 6, ("kiwis",))

# Solve the problem
solutions = problem.getSolutions()

# Find the fruit at rank 5 (third-most-expensive: 7=most, 6=second-most, 5=third-most)
for solution in solutions:
    for choice_letter, fruit_name in zip("ABCDEFG", ["kiwis", "cantaloupes", "oranges", "loquats", "pears", "watermelons", "peaches"]):
        if solution[fruit_name] == 5:
            print(choice_letter)