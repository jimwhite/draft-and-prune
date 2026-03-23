from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define the variables (the seven vehicles) and their age ranks (1=oldest, 7=newest)
vehicles = ["convertible", "truck", "tractor", "limousine", "motorcyle", "hatchback", "sedan"]
ranks = range(1, 8)
problem.addVariables(vehicles, ranks)

# Add constraints based on the puzzle's statements
# 1. All vehicles must have a different age rank.
problem.addConstraint(AllDifferentConstraint())

# 2. "The hatchback is the fourth-newest." (4th newest = rank 4)
problem.addConstraint(lambda hatchback: hatchback == 4, ("hatchback",))

# 3. "The limousine is older than the motorcyle."
problem.addConstraint(lambda limousine, motorcyle: limousine < motorcyle, ("limousine", "motorcyle"))

# 4. "The truck is newer than the motorcyle."
problem.addConstraint(lambda truck, motorcyle: truck > motorcyle, ("truck", "motorcyle"))

# 5. "The sedan is the second-newest." (2nd newest = rank 6)
problem.addConstraint(lambda sedan: sedan == 6, ("sedan",))

# 6. "The tractor is newer than the convertible."
problem.addConstraint(lambda tractor, convertible: tractor > convertible, ("tractor", "convertible"))

# 7. "The hatchback is older than the convertible."
problem.addConstraint(lambda hatchback, convertible: hatchback < convertible, ("hatchback", "convertible"))

# Find the solution(s)
solutions = problem.getSolutions()

# The question asks which vehicle is the "third-newest"
# In our ranking system (1=oldest, 7=newest), third-newest = rank 5
choices = {
    "A": "convertible",
    "B": "truck",
    "C": "tractor",
    "D": "limousine",
    "E": "motorcyle",
    "F": "hatchback",
    "G": "sedan"
}

# Find the vehicle with rank 5 and print its corresponding letter
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 5:
            print(letter)