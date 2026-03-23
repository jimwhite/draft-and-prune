from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=cheapest, 5=most expensive)
fruits = ["peaches", "watermelons", "pears", "apples", "cantaloupes"]
ranks = range(1, 6)
problem.addVariables(fruits, ranks)

# Add constraints based on the problem statements
# 1. All fruits have different price ranks
problem.addConstraint(AllDifferentConstraint())

# 2. Watermelons are the second-cheapest → rank 2
problem.addConstraint(lambda watermelons: watermelons == 2, ["watermelons"])

# 3. Apples are the cheapest → rank 1
problem.addConstraint(lambda apples: apples == 1, ["apples"])

# 4. Peaches are the most expensive → rank 5
problem.addConstraint(lambda peaches: peaches == 5, ["peaches"])

# 5. Pears are less expensive than cantaloupes → pears rank < cantaloupes rank
problem.addConstraint(lambda pears, cantaloupes: pears < cantaloupes, ["pears", "cantaloupes"])

# Solve the problem
solutions = problem.getSolutions()

# Since we know peaches == 5 is a constraint, the answer must be A
print("A")