from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (the three fruits) and domain (price ranks)
fruits = ["cantaloupe", "apple", "loquat"]
ranks = [1, 2, 3]  # 1=cheapest, 2=middle, 3=most expensive
problem.addVariables(fruits, ranks)

# Add constraints based on the problem description
# 1. All fruits must have different price ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The loquats are more expensive than the apples" → loquat > apple
problem.addConstraint(lambda loquat, apple: loquat > apple, ("loquat", "apple"))

# 3. "The cantaloupes are less expensive than the apples" → cantaloupe < apple
problem.addConstraint(lambda cantaloupe, apple: cantaloupe < apple, ("cantaloupe", "apple"))

# Solve the problem
solutions = problem.getSolutions()

# Map choices to fruits
choices = {
    "A": "cantaloupe",
    "B": "apple",
    "C": "loquat"
}

# Find which fruit has rank 3 (most expensive)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 3:
            print(letter)