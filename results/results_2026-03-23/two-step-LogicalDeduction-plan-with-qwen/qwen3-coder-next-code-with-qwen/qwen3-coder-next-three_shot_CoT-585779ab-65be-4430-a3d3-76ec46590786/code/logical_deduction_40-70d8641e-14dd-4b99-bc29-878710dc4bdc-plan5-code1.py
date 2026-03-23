from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=cheapest, 5=most expensive)
fruits = ["cantaloupe", "kiwi", "orange", "mango", "peach"]
ranks = range(1, 6)
problem.addVariables(fruits, ranks)

# Add constraints based on the problem description
# 1. All fruits have different price ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The kiwis are less expensive than the mangoes" → kiwi < mango
problem.addConstraint(lambda kiwi, mango: kiwi < mango, ("kiwi", "mango"))

# 3. "The peaches are less expensive than the oranges" → peach < orange
problem.addConstraint(lambda peach, orange: peach < orange, ("peach", "orange"))

# 4. "The oranges are the second-most expensive" → orange's rank = 4
problem.addConstraint(lambda orange: orange == 4, ("orange",))

# 5. "The mangoes are the second-cheapest" → mango's rank = 2
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

# Find which fruit has rank 2 (second-cheapest) and print the corresponding letter
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 2:
            print(letter)