from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (fruits) and domain (price ranks: 1=cheapest, 7=most expensive)
fruits = ["oranges", "plums", "loquats", "apples", "kiwis", "cantaloupes", "peaches"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add constraints based on the problem description
# 1. All fruits have different price ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The loquats are less expensive than the kiwis" → loquats < kiwis
problem.addConstraint(lambda loquats, kiwis: loquats < kiwis, ("loquats", "kiwis"))

# 3. "The plums are the cheapest" → plums == 1
problem.addConstraint(lambda plums: plums == 1, ("plums",))

# 4. "The loquats are the fourth-most expensive" → loquats == 4
problem.addConstraint(lambda loquats: loquats == 4, ("loquats",))

# 5. "The peaches are less expensive than the oranges" → peaches < oranges
problem.addConstraint(lambda peaches, oranges: peaches < oranges, ("peaches", "oranges"))

# 6. "The peaches are more expensive than the kiwis" → kiwis < peaches
problem.addConstraint(lambda kiwis, peaches: kiwis < peaches, ("kiwis", "peaches"))

# 7. "The apples are the second-cheapest" → apples == 2
problem.addConstraint(lambda apples: apples == 2, ("apples",))

# Solve the problem
solutions = problem.getSolutions()

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

# Find the fruit with rank 6 (second-most expensive)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 6:
            print(letter)