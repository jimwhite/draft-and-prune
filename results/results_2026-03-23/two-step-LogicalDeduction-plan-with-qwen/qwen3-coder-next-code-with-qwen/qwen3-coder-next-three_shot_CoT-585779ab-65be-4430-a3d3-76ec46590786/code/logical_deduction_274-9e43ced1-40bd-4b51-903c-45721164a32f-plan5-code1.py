from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (the three fruits) and domain (price ranks: 1=cheapest, 3=most expensive)
fruits = ["peaches", "pears", "mangoes"]
ranks = range(1, 4)
problem.addVariables(fruits, ranks)

# Add constraints based on the puzzle's statements
# 1. All fruits must have different price ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The peaches are the cheapest." → peach rank = 1
problem.addConstraint(lambda peaches: peaches == 1, ["peaches"])

# 3. "The mangoes are less expensive than the pears." → mango rank < pear rank
problem.addConstraint(lambda mangoes, pears: mangoes < pears, ["mangoes", "pears"])

# Solve for the arrangement
solutions = problem.getSolutions()

# Since we know peaches == 1 is enforced, choice A is correct
print("A")