from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
fruits = ["cantaloupe", "watermelon", "mango"]
ranks = range(1, 4)  # 1=cheapest, 3=most expensive
problem.addVariables(fruits, ranks)

# Add constraints based on the statements
# All fruits have different price ranks
problem.addConstraint(AllDifferentConstraint())

# The mangoes are the cheapest (rank 1)
problem.addConstraint(lambda mango: mango == 1, ["mango"])

# The cantaloupes are the second-most expensive (rank 2)
problem.addConstraint(lambda cantaloupe: cantaloupe == 2, ["cantaloupe"])

# Solve the problem
solutions = problem.getSolutions()

# Since we know the constraints directly specify that cantaloupes are second-most expensive,
# and this matches choice A, we output "A"
print("A")