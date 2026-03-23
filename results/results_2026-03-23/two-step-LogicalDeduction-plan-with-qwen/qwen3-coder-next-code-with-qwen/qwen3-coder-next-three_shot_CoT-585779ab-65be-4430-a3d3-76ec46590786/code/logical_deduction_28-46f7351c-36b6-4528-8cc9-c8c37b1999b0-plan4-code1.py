from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (vehicles) and domain (ranks: 1=newest, 5=oldest)
vehicles = ["convertible", "bus", "minivan", "truck", "sedan"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

# Add constraints based on the problem statements
# 1. All vehicles have different ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The convertible is newer than the truck" → convertible < truck
problem.addConstraint(lambda convertible, truck: convertible < truck, ("convertible", "truck"))

# 3. "The minivan is the newest" → minivan == 1
problem.addConstraint(lambda minivan: minivan == 1, ("minivan",))

# 4. "The bus is the third-newest" → bus == 3
problem.addConstraint(lambda bus: bus == 3, ("bus",))

# 5. "The truck is newer than the sedan" → truck < sedan
problem.addConstraint(lambda truck, sedan: truck < sedan, ("truck", "sedan"))

# Solve the problem
solutions = problem.getSolutions()

# Map choices to vehicles
choices = {
    "A": "convertible",
    "B": "bus",
    "C": "minivan",
    "D": "truck",
    "E": "sedan"
}

# Find which vehicle has rank 2 (second-newest)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 2:
            print(letter)