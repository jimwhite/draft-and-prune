from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (the three fruits) and domain (price ranks: 1=cheapest, 3=most expensive)
fruits = ["peaches", "pears", "mangoes"]
ranks = range(1, 4)
problem.addVariables(fruits, ranks)

# Add constraints based on the problem description
# 1. All fruits must have different price ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The mangoes are less expensive than the pears" → mangoes rank < pears rank
problem.addConstraint(lambda mangoes, pears: mangoes < pears, ("mangoes", "pears"))

# 3. "The peaches are the cheapest" → peaches rank = 1
problem.addConstraint(lambda peaches: peaches == 1, ("peaches",))

# Solve for the unique arrangement
solutions = problem.getSolutions()

# Since we know peaches == 1 is a constraint, choice A directly states this
# Verify and output the answer
if solutions:
    solution = solutions[0]
    if solution["peaches"] == 1:
        print("A")