from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define the variables (the seven fruits) and the domain (their price rank)
# Let's use ranks 1 to 7, where 1 is the cheapest and 7 is the most expensive.
fruits = ["apples", "pears", "mangoes", "oranges", "watermelons", "peaches", "cantaloupes"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add constraints based on the puzzle's statements
# 1. All fruits must have a different price rank.
problem.addConstraint(AllDifferentConstraint())

# 2. "The pears are more expensive than the oranges." (pears > oranges)
problem.addConstraint(lambda pears, oranges: pears > oranges, ("pears", "oranges"))

# 3. "The oranges are more expensive than the cantaloupes." (oranges > cantaloupes)
problem.addConstraint(lambda oranges, cantaloupes: oranges > cantaloupes, ("oranges", "cantaloupes"))

# 4. "The peaches are less expensive than the cantaloupes." (peaches < cantaloupes)
problem.addConstraint(lambda peaches, cantaloupes: peaches < cantaloupes, ("peaches", "cantaloupes"))

# 5. "The apples are the third-cheapest." (rank = 3)
problem.addConstraint(lambda apples: apples == 3, ("apples",))

# 6. "The watermelons are the second-most expensive." (rank = 6, since most expensive = 7)
problem.addConstraint(lambda watermelons: watermelons == 6, ("watermelons",))

# 7. "The mangoes are the fourth-most expensive." (rank = 4, since 7-3=4)
problem.addConstraint(lambda mangoes: mangoes == 4, ("mangoes",))

# Find the unique solution to the problem
solutions = problem.getSolutions()

# The question asks which fruit is the "second-cheapest".
# In our ranking system (1=cheapest), the second-cheapest has a rank of 2.
choices = {
    "A": "apples",
    "B": "pears",
    "C": "mangoes",
    "D": "oranges",
    "E": "watermelons",
    "F": "peaches",
    "G": "cantaloupes"
}

# Check the solution to find the fruit with rank 2 and print the corresponding letter.
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 2:
            print(letter)