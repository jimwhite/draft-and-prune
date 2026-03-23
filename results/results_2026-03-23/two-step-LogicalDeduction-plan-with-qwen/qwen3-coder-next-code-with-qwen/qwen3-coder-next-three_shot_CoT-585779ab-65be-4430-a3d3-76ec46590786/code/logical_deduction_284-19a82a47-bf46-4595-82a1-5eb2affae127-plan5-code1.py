from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
fruits = ["cantaloupe", "apple", "loquat"]
ranks = range(1, 4)  # 1=cheapest, 3=most expensive
problem.addVariables(fruits, ranks)

# Add constraints based on the statements
# All fruits have different price ranks
problem.addConstraint(AllDifferentConstraint())

# The loquats are more expensive than the apples: loquat > apple
problem.addConstraint(lambda loquat, apple: loquat > apple, ("loquat", "apple"))

# The cantaloupes are less expensive than the apples: cantaloupe < apple
problem.addConstraint(lambda cantaloupe, apple: cantaloupe < apple, ("cantaloupe", "apple"))

# Solve the problem
solutions = problem.getSolutions()

# Determine which fruit is most expensive (rank 3)
for solution in solutions:
    if solution["cantaloupe"] == 3:
        print("A")
    elif solution["apple"] == 3:
        print("B")
    elif solution["loquat"] == 3:
        print("C")