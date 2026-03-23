from constraint import *

problem = Problem()

golfers = ["amy", "eli", "eve"]
positions = range(1, 4)
problem.addVariables(golfers, positions)

problem.addConstraint(AllDifferentConstraint())

problem.addConstraint(lambda eve, amy: eve < amy, ["eve", "amy"])

problem.addConstraint(lambda eli, amy: eli > amy, ["eli", "amy"])

solutions = problem.getSolutions()

choices = {
    "A": "amy",
    "B": "eli",
    "C": "eve"
}

for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 3:
            print(letter)