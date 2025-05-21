from z3 import *

# Entities
J, K, L, N, O, R = 0, 1, 2, 3, 4, 5
W, T, F = 0, 1, 2
M, A = 0, 1

# Variables
assistant_at_session = Array('assistant_at_session', IntSort(), IntSort())

# Solver
s = Solver()

# Constraints
s.add(And([And(assistant_at_session[i] >= 0, assistant_at_session[i] < 6) for i in range(6)])) # Domain
s.add(Distinct([assistant_at_session[i] for i in range(6)])) # Distinctness

s1, s2 = Ints('s1 s2')
s.add(ForAll([s1, s2], Implies(And(assistant_at_session[s1] == K, assistant_at_session[s2] == R, s1 >=0, s1 < 6, s2 >= 0, s2 < 6), s1/2 == s2/2))) # Kevin and Rebecca same day
s.add(ForAll([s1, s2], Implies(And(assistant_at_session[s1] == L, assistant_at_session[s2] == O, s1 >=0, s1 < 6, s2 >= 0, s2 < 6), s1/2 != s2/2))) # Lan and Olivia different days

s.add(Or(assistant_at_session[1] == N, assistant_at_session[3] == N, assistant_at_session[5] == N)) # Nessa afternoon
s.add(ForAll([s1, s2], Implies(And(assistant_at_session[s1] == J, assistant_at_session[s2] == O, s1 >=0, s1 < 6, s2 >= 0, s2 < 6), s1/2 < s2/2))) # Julio before Olivia


# Specific condition
s.add(assistant_at_session[3] == J)

# Count determined assistants
determined_count = 0
other_assistants = [K, L, N, O, R]

for A in other_assistants:
    forced_session_count_for_A = 0
    for S in range(6):
        temp_s = Solver()
        temp_s.add(s.assertions())
        temp_s.add(assistant_at_session[S] != A)
        if temp_s.check() == unsat:
            forced_session_count_for_A += 1
    if forced_session_count_for_A == 1:
        determined_count += 1

# Map count to answer choice
answers = ["one", "two", "three", "four", "five"]
print(f"Option {chr(65 + answers.index(answers[determined_count -1]))} is correct")