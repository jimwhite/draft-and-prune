from z3 import *

# Employees: R, S, T, V, X, Y
# Parking Spaces: 1, 2, 3, 4, 5, 6

R, S, T, V, X, Y = Ints('R S T V X Y')
employees = [R, S, T, V, X, Y]
solver = Solver()

# Each employee gets a unique parking space from 1 to 6
solver.add(Distinct(employees))
for e in employees:
    solver.add(And(e >= 1, e <= 6))

# Constraints
solver.add(Y > T)
solver.add(X > S)
solver.add(R > Y)
solver.add(Or(R == 1, R == 2, R == 3, R == 4))


# Check if any employee is limited to only two possible spaces
def check_two_spaces(employee):
    possible_spaces = 0
    for space in range(1, 7):
        solver.push()
        solver.add(employee == space)
        if solver.check() == sat:
            possible_spaces += 1
        solver.pop()
    return possible_spaces == 2

num_employees_limited_to_two_spaces = 0
for employee in employees:
    if check_two_spaces(employee):
        num_employees_limited_to_two_spaces += 1

if num_employees_limited_to_two_spaces == 0:
    print("Option A is correct")
elif num_employees_limited_to_two_spaces == 2:
    print("Option B is correct")
elif num_employees_limited_to_two_spaces == 3:
    print("Option C is correct")
elif num_employees_limited_to_two_spaces == 4:
    print("Option D is correct")
elif num_employees_limited_to_two_spaces == 5:
    print("Option E is correct")