from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (fruits) and domain (ranks 1-7, where 1=cheapest, 7=most expensive)
fruits = ["oranges", "plums", "loquats", "apples", "kiwis", "cantaloupes", "peaches"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "The loquats are less expensive than the kiwis" → loquats < kiwis
problem.addConstraint(lambda loquats, kiwis: loquats < kiwis, ("loquats", "kiwis"))

# "The plums are the cheapest" → plums == 1
problem.addConstraint(lambda plums: plums == 1, ("plums",))

# "The loquats are the fourth-most expensive" → loquats == 4
problem.addConstraint(lambda loquats: loquats == 4, ("loquats",))

# "The peaches are less expensive than the oranges" → peaches < oranges
problem.addConstraint(lambda peaches, oranges: peaches < oranges, ("peaches", "oranges"))

# "The peaches are more expensive than the kiwis" → peaches > kiwis
problem.addConstraint(lambda peaches, kiwis: peaches > kiwis, ("peaches", "kiwis"))

# "The apples are the second-cheapest" → apples == 2
problem.addConstraint(lambda apples: apples == 2, ("apples",))

# Solve the problem
solutions = problem.getSolutions()

# The third-most-expensive corresponds to rank 5 (1=cheapest, 2=second-cheapest, 3=third-cheapest,
# 4=fourth-cheapest/fifth-most-expensive, 5=third-most-expensive)
# In ascending order: 1 (cheapest), 2, 3, 4, 5 (third-most-expensive), 6, 7 (most expensive)

# Map choice letters to fruit names
choices = {
    "A": "oranges",
    "B": "plums",
    "C": "loquats",
    "D": "apples",
    "E": "kiwis",
    "F": "cantaloupes",
    "G": "peaches"
}

# Find the fruit with rank 5 and print its corresponding choice letter
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 5:
            print(letter)