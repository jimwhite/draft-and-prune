from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (the seven fruits) and domain (price ranks 1 to 7, where 1=cheapest, 7=most expensive)
fruits = ["apples", "pears", "mangoes", "oranges", "watermelons", "peaches", "cantaloupes"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add constraints based on the problem description
# 1. All fruits have different price ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The pears are more expensive than the oranges" → pears rank < oranges rank
problem.addConstraint(lambda pears, oranges: pears < oranges, ("pears", "oranges"))

# 3. "The oranges are more expensive than the cantaloupes" → oranges rank < cantaloupes rank
problem.addConstraint(lambda oranges, cantaloupes: oranges < cantaloupes, ("oranges", "cantaloupes"))

# 4. "The peaches are less expensive than the cantaloupes" → cantaloupes rank < peaches rank
problem.addConstraint(lambda cantaloupes, peaches: cantaloupes < peaches, ("cantaloupes", "peaches"))

# 5. "The apples are the third-cheapest" → apples rank = 3
problem.addConstraint(lambda apples: apples == 3, ("apples",))

# 6. "The watermelons are the second-most expensive" → watermelons rank = 6
problem.addConstraint(lambda watermelons: watermelons == 6, ("watermelons",))

# 7. "The mangoes are the fourth-most expensive" → mangoes rank = 4
problem.addConstraint(lambda mangoes: mangoes == 4, ("mangoes",))

# Solve the problem
solutions = problem.getSolutions()

# The question asks which fruit is the fourth-most expensive (rank 4)
# According to the constraint, mangoes should be rank 4
# We'll verify this and output the corresponding choice letter

# Map choices to fruit names
choices = {
    "A": "apples",
    "B": "pears",
    "C": "mangoes",
    "D": "oranges",
    "E": "watermelons",
    "F": "peaches",
    "G": "cantaloupes"
}

# Find which fruit has rank 4 and print the corresponding letter
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 4:
            print(letter)