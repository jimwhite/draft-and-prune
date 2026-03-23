from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=cheapest, 5=most expensive)
fruits = ["cantaloupe", "kiwi", "orange", "mango", "peach"]
ranks = range(1, 6)
problem.addVariables(fruits, ranks)

# Add AllDifferentConstraint to ensure unique price ranks
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem statements:
# 1. "The kiwis are less expensive than the mangoes" → kiwi < mango
problem.addConstraint(lambda kiwi, mango: kiwi < mango, ("kiwi", "mango"))

# 2. "The peaches are less expensive than the oranges" → peach < orange
problem.addConstraint(lambda peach, orange: peach < orange, ("peach", "orange"))

# 3. "The oranges are the second-most expensive" → orange = 4
problem.addConstraint(lambda orange: orange == 4, ("orange",))

# 4. "The mangoes are the second-cheapest" → mango = 2
problem.addConstraint(lambda mango: mango == 2, ("mango",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to fruit names
choices = {
    "A": "cantaloupe",
    "B": "kiwi",
    "C": "orange",
    "D": "mango",
    "E": "peach"
}

# Find the fruit with rank 3 (third-most expensive)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 3:
            print(letter)