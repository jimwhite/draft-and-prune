from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define the variables (the seven fruits) and their domain (price rank)
# 1 = cheapest, 7 = most expensive
fruits = ["loquats", "peaches", "watermelons", "plums", "kiwis", "mangoes", "pears"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add constraints based on the puzzle's statements
# 1. All fruits must have a different price rank.
problem.addConstraint(AllDifferentConstraint())

# 2. "The pears are more expensive than the kiwis." → pears > kiwis
problem.addConstraint(lambda pears, kiwis: pears > kiwis, ("pears", "kiwis"))

# 3. "The watermelons are less expensive than the peaches." → watermelons < peaches
problem.addConstraint(lambda watermelons, peaches: watermelons < peaches, ("watermelons", "peaches"))

# 4. "The mangoes are the third-cheapest." → rank = 3
problem.addConstraint(lambda mangoes: mangoes == 3, ("mangoes",))

# 5. "The watermelons are the third-most expensive." → rank = 5 (since 7=most, 6=second-most, 5=third-most)
problem.addConstraint(lambda watermelons: watermelons == 5, ("watermelons",))

# 6. "The plums are the second-most expensive." → rank = 6
problem.addConstraint(lambda plums: plums == 6, ("plums",))

# 7. "The loquats are the second-cheapest." → rank = 2
problem.addConstraint(lambda loquats: loquats == 2, ("loquats",))

# Find the solution(s)
solutions = problem.getSolutions()

# Map choice letters to fruit names
choices = {
    "A": "loquats",
    "B": "peaches",
    "C": "watermelons",
    "D": "plums",
    "E": "kiwis",
    "F": "mangoes",
    "G": "pears"
}

# Find which fruit has rank 4 (fourth-most expensive)
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 4:
            print(letter)