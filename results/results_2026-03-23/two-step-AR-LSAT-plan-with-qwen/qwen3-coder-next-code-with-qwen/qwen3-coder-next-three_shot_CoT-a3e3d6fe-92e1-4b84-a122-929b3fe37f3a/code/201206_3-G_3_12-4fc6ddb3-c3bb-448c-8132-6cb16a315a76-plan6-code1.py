from z3 import *

# Representative indices: Kim=0, Mahr=1, Parra=2, Quinn=3, Stuckey=4, Tiao=5, Udall=6
zone = [Int(f"zone_{i}") for i in range(7)]

# Base solver
solver = Solver()

# Zone domain constraints: each zone is 1, 2, or 3
for i in range(7):
    solver.add(Or(zone[i] == 1, zone[i] == 2, zone[i] == 3))

# Condition (a): Exactly one of Parra or Tiao is in Zone 1
solver.add(Xor(zone[2] == 1, zone[5] == 1))

# Condition (b): Exactly one of Tiao or Udall is in Zone 2
solver.add(Xor(zone[5] == 2, zone[6] == 2))

# Condition (c): Parra and Quinn are in the same zone
solver.add(zone[2] == zone[3])

# Condition (d): Stuckey and Udall are in the same zone
solver.add(zone[4] == zone[6])

# Condition (e): Zone 3 has more representatives than Zone 2
count_zone3 = Sum([If(zone[i] == 3, 1, 0) for i in range(7)])
count_zone2 = Sum([If(zone[i] == 2, 1, 0) for i in range(7)])
solver.add(count_zone3 > count_zone2)

# Answer choices
answer_choices = [
    # Zone 1: Kim, Parra; Zone 2: Stuckey, Udall; Zone 3: Mahr, Quinn, Tiao
    [1, 0, 1, 3, 2, 3, 2],  # Kim=0->1, Mahr=1->0 (invalid), Parra=2->1, Quinn=3->3, Stuckey=4->2, Tiao=5->3, Udall=6->2
    # Zone 1: Kim, Tiao; Zone 2: Stuckey, Udall; Zone 3: Mahr, Parra, Quinn
    [1, 0, 3, 3, 2, 1, 2],  # Kim=0->1, Mahr=1->0 (invalid), Parra=2->3, Quinn=3->3, Stuckey=4->2, Tiao=5->1, Udall=6->2
    # Zone 1: Parra, Quinn; Zone 2: Kim, Udall; Zone 3: Mahr, Stuckey, Tiao
    [0, 0, 1, 1, 3, 3, 2],  # Kim=0->0 (invalid), Mahr=1->0 (invalid), Parra=2->1, Quinn=3->1, Stuckey=4->3, Tiao=5->3, Udall=6->2
    # Zone 1: Stuckey, Udall; Zone 2: Kim, Tiao; Zone 3: Mahr, Parra, Quinn
    [0, 0, 3, 3, 1, 2, 1],  # Kim=0->0 (invalid), Mahr=1->0 (invalid), Parra=2->3, Quinn=3->3, Stuckey=4->1, Tiao=5->2, Udall=6->1
    # Zone 1: Tiao; Zone 2: Kim, Parra, Quinn; Zone 3: Stuckey, Udall
    [0, 0, 2, 2, 3, 1, 3]   # Kim=0->0 (invalid), Mahr=1->0 (invalid), Parra=2->2, Quinn=3->2, Stuckey=4->3, Tiao=5->1, Udall=6->3
]

# Correct mapping for each choice (fixing invalid entries above)
# Choice 0: Kim=1, Parra=1, Stuckey=2, Udall=2, Mahr=3, Quinn=3, Tiao=3
choice0 = [1, 3, 1, 3, 2, 3, 2]
# Choice 1: Kim=1, Tiao=1, Stuckey=2, Udall=2, Mahr=3, Parra=3, Quinn=3
choice1 = [1, 3, 3, 3, 2, 1, 2]
# Choice 2: Parra=1, Quinn=1, Kim=2, Udall=2, Mahr=3, Stuckey=3, Tiao=3
choice2 = [2, 3, 1, 1, 3, 3, 2]
# Choice 3: Stuckey=1, Udall=1, Kim=2, Tiao=2, Mahr=3, Parra=3, Quinn=3
choice3 = [2, 3, 3, 3, 1, 2, 1]
# Choice 4: Tiao=1, Kim=2, Parra=2, Quinn=2, Stuckey=3, Udall=3
choice4 = [2, 0, 2, 2, 3, 1, 3]  # Mahr=0 is invalid; fix to any valid zone (e.g., 3)

# Actually, let's recompute each choice properly:
# Choice 0: Zone1=[Kim,Parra], Zone2=[Stuckey,Udall], Zone3=[Mahr,Quinn,Tiao]
#   Kim=0->1, Mahr=1->3, Parra=2->1, Quinn=3->3, Stuckey=4->2, Tiao=5->3, Udall=6->2
choice0 = [1, 3, 1, 3, 2, 3, 2]
# Choice 1: Zone1=[Kim,Tiao], Zone2=[Stuckey,Udall], Zone3=[Mahr,Parra,Quinn]
#   Kim=0->1, Mahr=1->3, Parra=2->3, Quinn=3->3, Stuckey=4->2, Tiao=5->1, Udall=6->2
choice1 = [1, 3, 3, 3, 2, 1, 2]
# Choice 2: Zone1=[Parra,Quinn], Zone2=[Kim,Udall], Zone3=[Mahr,Stuckey,Tiao]
#   Kim=0->2, Mahr=1->3, Parra=2->1, Quinn=3->1, Stuckey=4->3, Tiao=5->3, Udall=6->2
choice2 = [2, 3, 1, 1, 3, 3, 2]
# Choice 3: Zone1=[Stuckey,Udall], Zone2=[Kim,Tiao], Zone3=[Mahr,Parra,Quinn]
#   Kim=0->2, Mahr=1->3, Parra=2->3, Quinn=3->3, Stuckey=4->1, Tiao=5->2, Udall=6->1
choice3 = [2, 3, 3, 3, 1, 2, 1]
# Choice 4: Zone1=[Tiao], Zone2=[Kim,Parra,Quinn], Zone3=[Stuckey,Udall]
#   Kim=0->2, Mahr=1->3 (or 1 or 2), Parra=2->2, Quinn=3->2, Stuckey=4->3, Tiao=5->1, Udall=6->3
#   Let's set Mahr=3 (Zone 3)
choice4 = [2, 3, 2, 2, 3, 1, 3]

# Check each answer choice
valid_indices = []
for idx, assignment in enumerate([choice0, choice1, choice2, choice3, choice4]):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add the specific assignment
    for i in range(7):
        s_chk.add(zone[i] == assignment[i])
    
    if s_chk.check() == sat:
        valid_indices.append(idx)

print(valid_indices)