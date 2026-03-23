from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (the seven fruits) and domain (price ranks: 1=cheapest, 7=most expensive)
fruits = ["watermelons", "mangoes", "kiwis", "pears", "cantaloupes", "oranges", "peaches"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add constraints based on the puzzle's statements
# 1. All fruits must have a unique price rank
problem.addConstraint(AllDifferentConstraint())

# 2. "The oranges are more expensive than the peaches" → oranges_rank > peaches_rank
problem.addConstraint(lambda oranges, peaches: oranges > peaches, ("oranges", "peaches"))

# 3. "The cantaloupes are the fourth-most expensive" → cantaloupes = 4
problem.addConstraint(lambda cantaloupes: cantaloupes == 4, ("cantaloupes",))

# 4. "The pears are less expensive than the cantaloupes" → pears_rank < cantaloupes_rank
problem.addConstraint(lambda pears, cantaloupes: pears < cantaloupes, ("pears", "cantaloupes"))

# 5. "The peaches are the second-most expensive" → peaches = 6
problem.addConstraint(lambda peaches: peaches == 6, ("peaches",))

# 6. "The mangoes are the cheapest" → mangoes = 1
problem.addConstraint(lambda mangoes: mangoes == 1, ("mangoes",))

# 7. "The kiwis are the third-cheapest" → kiwis = 3
problem.addConstraint(lambda kiwis: kiwis == 3, ("kiwis",))

# Find the unique solution
solutions = problem.getSolutions()

# Map choice letters to fruit names for second-most expensive (rank 6)
choices = {
    "A": "watermelons",
    "B": "mangoes",
    "C": "kiwis",
    "D": "pears",
    "E": "cantaloupes",
    "F": "oranges",
    "G": "peaches"
}

# Find which fruit has rank 6 (second-most expensive)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 6:
            print(letter)