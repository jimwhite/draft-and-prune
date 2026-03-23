from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define the variables (the seven fruits) and the domain (their price rank)
# Rank 1 = cheapest, rank 7 = most expensive
fruits = ["mangoes", "kiwis", "oranges", "watermelons", "apples", "pears", "loquats"]
ranks = range(1, 8)
problem.addVariables(fruits, ranks)

# Add constraints based on the puzzle's statements
# 1. All fruits must have a different price rank.
problem.addConstraint(AllDifferentConstraint())

# 2. "The loquats are less expensive than the oranges." (loquats < oranges)
problem.addConstraint(lambda loquats, oranges: loquats < oranges, ("loquats", "oranges"))

# 3. "The oranges are the third-most expensive." (rank = 5, since 7 is most expensive)
problem.addConstraint(lambda oranges: oranges == 5, ("oranges",))

# 4. "The apples are the cheapest." (rank = 1)
problem.addConstraint(lambda apples: apples == 1, ("apples",))

# 5. "The kiwis are more expensive than the pears." (kiwis > pears)
problem.addConstraint(lambda kiwis, pears: kiwis > pears, ("kiwis", "pears"))

# 6. "The mangoes are more expensive than the watermelons." (mangoes > watermelons)
problem.addConstraint(lambda mangoes, watermelons: mangoes > watermelons, ("mangoes", "watermelons"))

# 7. "The loquats are more expensive than the kiwis." (loquats > kiwis)
problem.addConstraint(lambda loquats, kiwis: loquats > kiwis, ("loquats", "kiwis"))

# Find the unique solution to the problem
solutions = problem.getSolutions()

# The question asks which fruit is the "fourth-most expensive"
# In our ranking system (1=cheapest, 7=most expensive), fourth-most expensive corresponds to rank 4
choices = {
    "A": "mangoes",
    "B": "kiwis",
    "C": "oranges",
    "D": "watermelons",
    "E": "apples",
    "F": "pears",
    "G": "loquats"
}

# Check the solution to find which fruit has rank 4 and print its corresponding letter
for solution in solutions:
    for letter, fruit_name in choices.items():
        if solution[fruit_name] == 4:
            print(letter)