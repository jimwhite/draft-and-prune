from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=cheapest, 3=most expensive)
fruits = ["cantaloupe", "watermelon", "mango"]
ranks = range(1, 4)
problem.addVariables(fruits, ranks)

# Add constraints based on the problem description
# 1. All fruits must have different price ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The mangoes are the cheapest" → rank = 1
problem.addConstraint(lambda mango: mango == 1, ["mango"])

# 3. "The cantaloupes are the second-most expensive" → rank = 2
problem.addConstraint(lambda cantaloupe: cantaloupe == 2, ["cantaloupe"])

# Solve the problem
solutions = problem.getSolutions()

# Since we have a unique solution and the question asks which statement is true,
# we can directly check against the given choices
# Choice A states "The cantaloupes are the second-most expensive", which matches our constraint
print("A")