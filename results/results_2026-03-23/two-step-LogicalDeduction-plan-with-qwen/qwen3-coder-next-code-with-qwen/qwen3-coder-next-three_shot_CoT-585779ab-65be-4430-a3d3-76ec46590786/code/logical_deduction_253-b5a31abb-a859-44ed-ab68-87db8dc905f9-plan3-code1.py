from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=cheapest, 3=most expensive)
fruits = ["cantaloupe", "watermelon", "mango"]
ranks = range(1, 4)
problem.addVariables(fruits, ranks)

# Add constraints based on the problem description
# 1. All fruits have different price ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The mangoes are the cheapest."
problem.addConstraint(lambda mango: mango == 1, ["mango"])

# 3. "The cantaloupes are the second-most expensive."
problem.addConstraint(lambda cantaloupe: cantaloupe == 2, ["cantaloupe"])

# Solve the problem
solutions = problem.getSolutions()

# Since there's only one solution, get it directly
solution = solutions[0]

# Determine which choice is true based on the solution
# Choice A: "The cantaloupes are the second-most expensive." -> cantaloupe == 2
# Choice B: "The watermelons are the second-most expensive." -> watermelon == 2
# Choice C: "The mangoes are the second-most expensive." -> mango == 2

if solution["cantaloupe"] == 2:
    print("A")
elif solution["watermelon"] == 2:
    print("B")
elif solution["mango"] == 2:
    print("C")