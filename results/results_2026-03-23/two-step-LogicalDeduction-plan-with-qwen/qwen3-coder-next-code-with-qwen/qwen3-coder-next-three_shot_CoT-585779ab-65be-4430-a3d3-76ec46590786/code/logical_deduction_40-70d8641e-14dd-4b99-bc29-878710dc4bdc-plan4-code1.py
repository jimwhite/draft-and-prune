from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=cheapest, 5=most expensive)
fruits = ["cantaloupe", "kiwi", "orange", "mango", "peach"]
ranks = range(1, 6)
problem.addVariables(fruits, ranks)

# Add constraints
# All fruits have different price ranks
problem.addConstraint(AllDifferentConstraint())

# "The kiwis are less expensive than the mangoes" -> kiwi < mango
problem.addConstraint(lambda kiwi, mango: kiwi < mango, ("kiwi", "mango"))

# "The peaches are less expensive than the oranges" -> peach < orange
problem.addConstraint(lambda peach, orange: peach < orange, ("peach", "orange"))

# "The oranges are the second-most expensive" -> orange == 4 (since 5 is most expensive)
problem.addConstraint(lambda orange: orange == 4, ("orange",))

# "The mangoes are the second-cheapest" -> mango == 2 (since 1 is cheapest)
problem.addConstraint(lambda mango: mango == 2, ("mango",))

# Solve the problem
solutions = problem.getSolutions()

# Map choices to fruit names
choices = {
    "A": "cantaloupe",
    "B": "kiwi",
    "C": "orange",
    "D": "mango",
    "E": "peach"
}

# Find which fruit has rank 2 (second-cheapest)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 2:
            print(letter)