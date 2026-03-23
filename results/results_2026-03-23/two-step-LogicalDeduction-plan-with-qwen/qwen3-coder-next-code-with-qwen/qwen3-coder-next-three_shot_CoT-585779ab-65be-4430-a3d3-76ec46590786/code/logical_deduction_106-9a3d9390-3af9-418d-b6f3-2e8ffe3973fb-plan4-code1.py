from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define the variables (the seven fruits) and the domain (their price rank)
# Let's use ranks 1 to 7, where 1 is the cheapest and 7 is the most expensive.
fruits = ["watermelons", "cantaloupes", "pears", "peaches", "mangoes", "kiwis", "oranges"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add constraints based on the puzzle's statements
# 1. All fruits must have a different price rank.
problem.addConstraint(AllDifferentConstraint())

# 2. "The oranges are more expensive than the cantaloupes."
problem.addConstraint(lambda oranges, cantaloupes: oranges > cantaloupes, ("oranges", "cantaloupes"))

# 3. "The pears are less expensive than the kiwis."
problem.addConstraint(lambda pears, kiwis: pears < kiwis, ("pears", "kiwis"))

# 4. "The kiwis are the fourth-most expensive."
problem.addConstraint(lambda kiwis: kiwis == 4, ("kiwis",))

# 5. "The mangoes are less expensive than the pears."
problem.addConstraint(lambda mangoes, pears: mangoes < pears, ("mangoes", "pears"))

# 6. "The peaches are the cheapest."
problem.addConstraint(lambda peaches: peaches == 1, ("peaches",))

# 7. "The cantaloupes are more expensive than the watermelons."
problem.addConstraint(lambda cantaloupes, watermelons: cantaloupes > watermelons, ("cantaloupes", "watermelons"))

# Find the unique solution to the problem
solutions = problem.getSolutions()

# The question asks which fruit is the fourth-most expensive (rank 4).
choices = {
    "A": "watermelons",
    "B": "cantaloupes",
    "C": "pears",
    "D": "peaches",
    "E": "mangoes",
    "F": "kiwis",
    "G": "oranges"
}

# Check the solution to find which fruit has rank 4 and print its corresponding letter.
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 4:
            print(letter)