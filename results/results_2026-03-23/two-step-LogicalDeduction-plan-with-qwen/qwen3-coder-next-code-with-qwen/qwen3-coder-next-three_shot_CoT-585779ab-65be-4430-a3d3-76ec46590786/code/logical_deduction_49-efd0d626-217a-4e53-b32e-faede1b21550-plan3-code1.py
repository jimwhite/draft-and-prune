from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=cheapest, 5=most expensive)
fruits = ["peaches", "watermelons", "pears", "apples", "cantaloupes"]
ranks = range(1, 6)
problem.addVariables(fruits, ranks)

# Add constraints based on the problem statements
# 1. All fruits have unique price ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The watermelons are the second-cheapest" → rank = 2
problem.addConstraint(lambda watermelons: watermelons == 2, ["watermelons"])

# 3. "The apples are the cheapest" → rank = 1
problem.addConstraint(lambda apples: apples == 1, ["apples"])

# 4. "The peaches are the most expensive" → rank = 5
problem.addConstraint(lambda peaches: peaches == 5, ["peaches"])

# 5. "The pears are less expensive than the cantaloupes" → pears < cantaloupes
problem.addConstraint(lambda pears, cantaloupes: pears < cantaloupes, ["pears", "cantaloupes"])

# Solve the problem
solutions = problem.getSolutions()

# Since we know from constraint #4 that peaches == 5 (most expensive),
# option A ("The peaches are the most expensive") must be true.
# We can directly output "A" as the answer.
print("A")