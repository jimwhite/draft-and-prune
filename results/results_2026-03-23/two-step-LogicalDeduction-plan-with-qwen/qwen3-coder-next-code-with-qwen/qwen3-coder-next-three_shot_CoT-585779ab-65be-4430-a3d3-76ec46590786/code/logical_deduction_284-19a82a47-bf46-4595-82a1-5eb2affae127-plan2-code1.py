from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
fruits = ["cantaloupe", "apple", "loquat"]
ranks = range(1, 4)  # 1=least expensive, 2=middle, 3=most expensive
problem.addVariables(fruits, ranks)

# Add constraints based on the statements
# All fruits have different price ranks
problem.addConstraint(AllDifferentConstraint())

# "The loquats are more expensive than the apples" -> loquat > apple
problem.addConstraint(lambda loquat, apple: loquat > apple, ("loquat", "apple"))

# "The cantaloupes are less expensive than the apples" -> cantaloupe < apple
problem.addConstraint(lambda cantaloupe, apple: cantaloupe < apple, ("cantaloupe", "apple"))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to fruit names
choices = {
    "A": "cantaloupe",
    "B": "apple",
    "C": "loquat"
}

# Find which fruit is the most expensive (rank = 3)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 3:
            print(letter)