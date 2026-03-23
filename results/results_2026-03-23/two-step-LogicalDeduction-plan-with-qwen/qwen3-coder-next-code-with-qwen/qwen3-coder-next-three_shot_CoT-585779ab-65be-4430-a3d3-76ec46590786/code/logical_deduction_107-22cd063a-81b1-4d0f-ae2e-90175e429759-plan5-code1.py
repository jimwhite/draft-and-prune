from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define the variables (the seven fruits) and the domain (their price rank)
# Let's use ranks 1 to 7, where 1 is the cheapest and 7 is the most expensive.
fruits = ["kiwis", "cantaloupes", "oranges", "loquats", "pears", "watermelons", "peaches"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add constraints based on the puzzle's statements
# 1. All fruits must have a different price rank.
problem.addConstraint(AllDifferentConstraint())

# 2. "The loquats are less expensive than the peaches." (loquats < peaches)
problem.addConstraint(lambda loquats, peaches: loquats < peaches, ("loquats", "peaches"))

# 3. "The pears are the third-cheapest." (rank 3)
problem.addConstraint(lambda pears: pears == 3, ("pears",))

# 4. "The oranges are less expensive than the cantaloupes." (oranges < cantaloupes)
problem.addConstraint(lambda oranges, cantaloupes: oranges < cantaloupes, ("oranges", "cantaloupes"))

# 5. "The loquats are more expensive than the watermelons." (loquats > watermelons)
problem.addConstraint(lambda loquats, watermelons: loquats > watermelons, ("loquats", "watermelons"))

# 6. "The peaches are less expensive than the oranges." (peaches < oranges)
problem.addConstraint(lambda peaches, oranges: peaches < oranges, ("peaches", "oranges"))

# 7. "The kiwis are the second-most expensive." (With 7 items, rank 6)
problem.addConstraint(lambda kiwis: kiwis == 6, ("kiwis",))

# Find the unique solution to the problem
solutions = problem.getSolutions()

# The question asks which fruit is the "second-cheapest".
# In our ranking system (1=cheapest), the second-cheapest has a rank of 2.
choices = {
    "A": "kiwis",
    "B": "cantaloupes",
    "C": "oranges",
    "D": "loquats",
    "E": "pears",
    "F": "watermelons",
    "G": "peaches"
}

# Check the solution to find the fruit with rank 2 and print the corresponding letter.
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 2:
            print(letter)