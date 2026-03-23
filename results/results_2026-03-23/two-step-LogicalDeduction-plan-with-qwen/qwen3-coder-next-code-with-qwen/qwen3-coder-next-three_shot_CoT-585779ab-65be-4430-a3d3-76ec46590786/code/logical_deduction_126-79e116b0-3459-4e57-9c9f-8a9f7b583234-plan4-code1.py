from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define the seven vehicle variables and their rank domain (1=oldest, 7=newest)
vehicles = ["bus", "motorcyle", "hatchback", "station_wagon", "minivan", "truck", "limousine"]
ranks = range(1, 8)
problem.addVariables(vehicles, ranks)

# Add constraints based on the puzzle's statements
# 1. All vehicles must have a different rank
problem.addConstraint(AllDifferentConstraint())

# 2. "The station wagon is the fourth-newest." 
# Since 1=oldest and 7=newest, fourth-newest means rank 4 (positions from oldest: 1,2,3,4,5,6,7)
problem.addConstraint(lambda station_wagon: station_wagon == 4, ("station_wagon",))

# 3. "The motorcyle is newer than the truck." -> motorcyle > truck
problem.addConstraint(lambda motorcyle, truck: motorcyle > truck, ("motorcyle", "truck"))

# 4. "The station wagon is older than the hatchback." -> station_wagon < hatchback
problem.addConstraint(lambda station_wagon, hatchback: station_wagon < hatchback, ("station_wagon", "hatchback"))

# 5. "The minivan is newer than the hatchback." -> minivan > hatchback
problem.addConstraint(lambda minivan, hatchback: minivan > hatchback, ("minivan", "hatchback"))

# 6. "The bus is newer than the minivan." -> bus > minivan
problem.addConstraint(lambda bus, minivan: bus > minivan, ("bus", "minivan"))

# 7. "The truck is newer than the limousine." -> truck > limousine
problem.addConstraint(lambda truck, limousine: truck > limousine, ("truck", "limousine"))

# Find the solution(s)
solutions = problem.getSolutions()

# Map choice letters to vehicle names
choices = {
    "A": "bus",
    "B": "motorcyle",
    "C": "hatchback",
    "D": "station_wagon",
    "E": "minivan",
    "F": "truck",
    "G": "limousine"
}

# Find which vehicle has rank 6 (second-newest)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 6:
            print(letter)