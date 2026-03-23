from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 5, where 1 is leftmost)
birds = ["cardinal", "crow", "falcon", "robin", "blue jay"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add constraints
# All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# "The robin is to the right of the cardinal" → robin position > cardinal position
problem.addConstraint(lambda robin, cardinal: robin > cardinal, ["robin", "cardinal"])

# "The cardinal is to the right of the blue jay" → cardinal position > blue jay position
problem.addConstraint(lambda cardinal, blue_jay: cardinal > blue_jay, ["cardinal", "blue jay"])

# "The blue jay is the second from the left" → blue jay position == 2
problem.addConstraint(lambda blue_jay: blue_jay == 2, ["blue jay"])

# "The crow is the rightmost" → crow position == 5
problem.addConstraint(lambda crow: crow == 5, ["crow"])

# Solve the problem
solutions = problem.getSolutions()

# The question asks which bird is second from the left (position 2)
# According to our constraint, blue jay must be at position 2
# So choice E is directly supported by the constraint

# Even though we know it's E, let's verify with the solution
for solution in solutions:
    for letter, bird_name in [("A", "cardinal"), ("B", "crow"), ("C", "falcon"), 
                               ("D", "robin"), ("E", "blue jay")]:
        if solution[bird_name] == 2:
            print(letter)