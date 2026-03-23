from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (the seven fruits)
fruits = ["cantaloupes", "plums", "mangoes", "apples", "loquats", "pears", "peaches"]

# Define domain: 1 = cheapest, 7 = most expensive
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add constraints based on the problem description
# 1. All fruits have different prices (ranks)
problem.addConstraint(AllDifferentConstraint())

# 2. "The apples are less expensive than the cantaloupes" → apples < cantaloupes
problem.addConstraint(lambda apples, cantaloupes: apples < cantaloupes, ("apples", "cantaloupes"))

# 3. "The apples are more expensive than the peaches" → peaches < apples
problem.addConstraint(lambda peaches, apples: peaches < apples, ("peaches", "apples"))

# 4. "The mangoes are the fourth-most expensive" → rank 4
problem.addConstraint(lambda mangoes: mangoes == 4, ("mangoes",))

# 5. "The peaches are more expensive than the plums" → plums < peaches
problem.addConstraint(lambda plums, peaches: plums < peaches, ("plums", "peaches"))

# 6. "The pears are the third-most expensive" → rank 5 (7=1st, 6=2nd, 5=3rd)
problem.addConstraint(lambda pears: pears == 5, ("pears",))

# 7. "The loquats are the third-cheapest" → rank 3 (1=1st cheapest, 2=2nd, 3=3rd)
problem.addConstraint(lambda loquats: loquats == 3, ("loquats",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to fruit names for the question about fourth-most expensive (rank 4)
choices = {
    "A": "cantaloupes",
    "B": "plums",
    "C": "mangoes",
    "D": "apples",
    "E": "loquats",
    "F": "pears",
    "G": "peaches"
}

# Find which fruit has rank 4 and print the corresponding choice letter
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 4:
            print(letter)