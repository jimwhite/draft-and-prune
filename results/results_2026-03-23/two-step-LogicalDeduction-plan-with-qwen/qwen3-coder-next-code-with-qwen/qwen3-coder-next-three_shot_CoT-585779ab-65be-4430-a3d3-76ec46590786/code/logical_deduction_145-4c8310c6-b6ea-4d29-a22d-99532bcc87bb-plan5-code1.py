from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define the variables (the seven fruits) and the domain (their cost rank)
# Let's use ranks 1 to 7, where 1 is the cheapest and 7 is the most expensive.
fruits = ["mangoes", "cantaloupes", "apples", "plums", "loquats", "watermelons", "peaches"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add constraints based on the puzzle's statements
# 1. All fruits must have a different cost rank.
problem.addConstraint(AllDifferentConstraint())

# 2. "The plums are more expensive than the mangoes." (plums > mangoes)
problem.addConstraint(lambda plums, mangoes: plums > mangoes, ("plums", "mangoes"))

# 3. "The watermelons are more expensive than the loquats." (watermelons > loquats)
problem.addConstraint(lambda watermelons, loquats: watermelons > loquats, ("watermelons", "loquats"))

# 4. "The loquats are the second-cheapest." (rank 2)
problem.addConstraint(lambda loquats: loquats == 2, ("loquats",))

# 5. "The plums are less expensive than the peaches." (plums < peaches)
problem.addConstraint(lambda plums, peaches: plums < peaches, ("plums", "peaches"))

# 6. "The mangoes are the fourth-most expensive." (rank 4)
problem.addConstraint(lambda mangoes: mangoes == 4, ("mangoes",))

# 7. "The peaches are less expensive than the cantaloupes." (peaches < cantaloupes)
problem.addConstraint(lambda peaches, cantaloupes: peaches < cantaloupes, ("peaches", "cantaloupes"))

# Find the unique solution to the problem
solutions = problem.getSolutions()

# The question asks which fruit is the cheapest (rank 1)
choices = {
    "A": "mangoes",
    "B": "cantaloupes",
    "C": "apples",
    "D": "plums",
    "E": "loquats",
    "F": "watermelons",
    "G": "peaches"
}

# Check the solution to find which fruit has rank 1 and print its corresponding letter
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 1:
            print(letter)